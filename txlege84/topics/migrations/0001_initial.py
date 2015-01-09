# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('image', models.URLField(null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(default='D', max_length=1, choices=[('D', 'Draft'), ('P', 'Published'), ('W', 'Withdrawn')])),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('issue', models.ForeignKey(related_name='texts', to='topics.Issue')),
            ],
            options={
                'ordering': ('created_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoryPointer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('pub_date', models.DateField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('issue', models.ForeignKey(related_name='stories', to='topics.Issue')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('slug', models.SlugField()),
                ('curators', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopIssue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('issue', models.ForeignKey(related_name='top_issue', to='topics.Issue')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='active_text',
            field=models.ForeignKey(related_name='issues', to='topics.IssueText'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='related_bills',
            field=models.ManyToManyField(related_name='issues', null=True, to='bills.Bill', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='topic',
            field=models.ForeignKey(related_name='issues', to='topics.Topic'),
            preserve_default=True,
        ),
    ]
