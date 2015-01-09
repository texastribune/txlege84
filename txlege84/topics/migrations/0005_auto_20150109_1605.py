# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0004_auto_20150109_1516'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issuetext',
            options={'ordering': ('-created_date',)},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'verbose_name': 'hot list'},
        ),
    ]
