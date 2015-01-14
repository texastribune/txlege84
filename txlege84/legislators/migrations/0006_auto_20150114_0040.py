# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0005_legislator_tribune_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legislator',
            name='middle_name',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
    ]
