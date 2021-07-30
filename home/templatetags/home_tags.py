import requests
from django import template
from wagtail.core.models import Locale, Site

from home.models import FooterPage, SectionIndexPage
from iogt.settings.base import LANGUAGES

register = template.Library()


@register.inclusion_tag('home/tags/language_switcher.html')
def language_switcher(page):
    return {
        'translations': page.get_translations(inclusive=True).all(),

    }


@register.inclusion_tag('home/tags/previous-next-buttons.html')
def render_previous_next_buttons(page):
    return {
        'next_sibling': page.get_next_siblings().live().first(),
        'previous_sibling': page.get_prev_siblings().live().first()
    }


@register.inclusion_tag('home/tags/footer.html', takes_context=True)
def footer(context):
    return {
        'footer_pages': FooterPage.get_active_footers(),
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/top_level_sections.html', takes_context=True)
def top_level_sections(context):
    return {
        'top_level_sections': SectionIndexPage.get_top_level_sections(),
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/banners_list.html')
def render_banners_list(banners):
    return {'banners': banners}


@register.inclusion_tag('home/tags/articles_list.html')
def render_articles_list(articles):
    return {'articles': articles}


@register.inclusion_tag('home/tags/featured_content_list.html')
def render_featured_content_list(featured_content):
    return {'featured_content_items': featured_content}


@register.inclusion_tag('home/tags/sub_sections.html')
def render_sub_sections_list(sub_sections):
    return {'sub_sections': sub_sections}


@register.inclusion_tag('home/tags/polls.html')
def render_polls_list(polls):
    return {'polls': polls}


@register.inclusion_tag('home/tags/questionnaire.html')
def render_questionnaire_list(questionnaire):
    return {'questionnaire': questionnaire}


@register.inclusion_tag('home/tags/section_progress.html')
def render_user_progress(user_progress):
    return user_progress


@register.inclusion_tag('home/tags/sub_sections.html')
def render_sub_sections_list(sub_sections):
    return {'sub_sections': sub_sections}


@register.simple_tag
def locale_set(locale, url):
    for item in LANGUAGES:
        code = item[0]
        url = url.replace(f"/{code}/", "")
    return f'/{locale}/{url}'

@register.simple_tag
def translated_home_page_url(language_code):
    locale = Locale.objects.get(language_code=language_code)
    default_home_page = Site.objects.filter(is_default_site=True).first().root_page
    home_page = default_home_page.get_translation_or_none(locale)
    page = home_page or default_home_page
    return page.url


@register.inclusion_tag('home/tags/svg_icon.html')
def svg_image(request, url):
    abs_url = request.build_absolute_uri(url)
    response = requests.get(abs_url)
    return {'svg': response.content.decode('utf-8')}