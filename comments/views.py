from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django_comments.views.comments import post_comment
from django_comments_xtd.models import XtdComment
from django.utils.translation import ugettext as _

from comments.forms import AdminCommentForm
from comments.models import CannedResponse


def update(request, comment_pk, action):
    get_comment_with_children_filter = Q(parent_id=comment_pk) | Q(pk=comment_pk)
    comments = XtdComment.objects.filter(get_comment_with_children_filter)
    verb = ''
    if action == 'unpublish':
        for comment in comments:
            comment.is_public = False
        verb = 'unpublished'
    elif action == 'publish':
        for comment in comments:
            comment.is_public = True
        verb = 'published'
    elif action == 'hide':
        for comment in comments:
            comment.is_removed = True
        verb = 'removed'
    elif action == 'show':
        for comment in comments:
            comment.is_removed = False
        verb = 'shown'
    elif action == 'clear_flags':
        comment = XtdComment.objects.get(pk=comment_pk)
        comment.flags.all().delete()
        verb = 'cleared'
    XtdComment.objects.bulk_update(comments, ['is_public', 'is_removed'])

    messages.success(request, _(f'The comment has been {verb} successfully!'))

    return redirect(request.META.get('HTTP_REFERER'))


class CommentReplyView(TemplateView):
    template_name = 'comment_reply.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = XtdComment.objects.get(pk=kwargs['comment_pk'])
        context.update({
            'form': AdminCommentForm(comment.content_object, comment=comment),
            'comment': comment,
            'canned_responses': CannedResponse.objects.all()
        })
        return context


@csrf_protect
@require_POST
def post_admin_comment(request):
    """
    This is a hack to make the post comment view send a message. There
    was no better way to do this than use a decorator pattern. Suggestions/Improvements
    are welcome
    :param request:
    :return:
    """
    response = post_comment(request, next='/')
    messages.success(request, _("Sent Reply successfully"))
    return response
