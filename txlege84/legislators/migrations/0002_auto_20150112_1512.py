# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislator',
            name='tribune_city',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='legislator',
            name='tribune_photo',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='legislator',
            name='tribune_slug',
            field=models.SlugField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
