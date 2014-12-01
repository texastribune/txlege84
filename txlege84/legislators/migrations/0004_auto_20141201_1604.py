# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0003_auto_20141120_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legislator',
            name='party',
            field=models.ForeignKey(related_name='legislators', blank=True, to='legislators.Party', null=True),
            preserve_default=True,
        ),
    ]
