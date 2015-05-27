# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0006_auto_20150506_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='vetoed',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
