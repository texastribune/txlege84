# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0011_auto_20141222_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storypointer',
            name='active',
        ),
    ]
