# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0004_legislator_tribune_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislator',
            name='tribune_room',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
