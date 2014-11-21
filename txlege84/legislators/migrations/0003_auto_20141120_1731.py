# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0002_auto_20141120_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legislator',
            name='openstates_id',
            field=models.CharField(unique=True, max_length=9),
            preserve_default=True,
        ),
    ]
