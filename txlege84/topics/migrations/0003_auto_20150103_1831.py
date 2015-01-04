# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_topissue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
