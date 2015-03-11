# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0006_auto_20150114_0040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='legislator',
            options={'ordering': ('last_name',)},
        ),
    ]
