# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0006_auto_20141222_1425'),
    ]

    operations = [
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
            field=models.OneToOneField(default=0, to='topics.IssueText'),
            preserve_default=False,
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
    ]
