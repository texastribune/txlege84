# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legislator',
            name='chamber',
            field=models.ForeignKey(related_name='legislators', blank=True, to='legislators.Chamber', null=True),
            preserve_default=True,
        ),
    ]
