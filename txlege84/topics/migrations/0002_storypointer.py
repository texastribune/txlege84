# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryPointer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('order', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
                ('stream', models.ForeignKey(related_name='stories', to='topics.Stream')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
