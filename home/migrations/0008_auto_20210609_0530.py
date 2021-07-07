# Generated by Django 3.1.12 on 2021-06-09 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('home', '0007_bannerindexpage_bannerpage_featuredcontent_homepagebanner'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FooterPage',
            fields=[
                ('article_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.article')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.article',),
        ),
        migrations.DeleteModel(
            name='Footer',
        ),
    ]
