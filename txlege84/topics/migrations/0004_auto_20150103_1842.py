# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20150103_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topissue',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
