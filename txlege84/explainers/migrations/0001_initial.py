# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Explainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('youtube_id', models.CharField(max_length=11)),
                ('text', models.TextField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
    ]
