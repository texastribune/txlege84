# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_auto_20150113_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='sponsors',
        ),
    ]
