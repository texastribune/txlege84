# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0010_auto_20141222_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storypointer',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
