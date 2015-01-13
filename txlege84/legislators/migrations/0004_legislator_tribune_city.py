# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0003_legislator_tribune_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislator',
            name='tribune_city',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
    ]
