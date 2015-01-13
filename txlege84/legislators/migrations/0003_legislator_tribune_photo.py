# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0002_legislator_tribune_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislator',
            name='tribune_photo',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
