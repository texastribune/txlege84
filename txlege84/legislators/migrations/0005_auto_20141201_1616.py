# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0004_auto_20141201_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislator',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='legislator',
            name='profile_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
