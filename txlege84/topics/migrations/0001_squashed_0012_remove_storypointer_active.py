# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('order', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
                ('related_bills', models.ManyToManyField(related_name='issues', to=b'bills.Bill')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoryPointer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('order', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issue', models.OneToOneField(related_name='stream_of', to='topics.Issue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('curators', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='storypointer',
            name='stream',
            field=models.ForeignKey(related_name='stories', to='topics.Stream'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='topic',
            field=models.ForeignKey(related_name='issues', to='topics.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='slug',
            field=models.SlugField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='image',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='issue',
            name='active',
        ),
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.CharField(default='D', max_length=1, choices=[('D', 'Draft'), ('P', 'Published'), ('W', 'Withdrawn')]),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='IssueText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('associated_issue', models.ForeignKey(related_name='texts', to='topics.Issue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='issue',
            name='text',
        ),
        migrations.AddField(
            model_name='issue',
            name='active_text',
            field=models.OneToOneField(null=True, blank=True, to='topics.IssueText'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 22, 20, 53, 4, 669749, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 22, 20, 53, 8, 453798, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='storypointer',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='storypointer',
            name='active',
        ),
    ]
