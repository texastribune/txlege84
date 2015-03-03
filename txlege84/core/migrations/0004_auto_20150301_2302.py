# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150114_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='convenetime',
            name='status',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='convenetime',
            name='time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
