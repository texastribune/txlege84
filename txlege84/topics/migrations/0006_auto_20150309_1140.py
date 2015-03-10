# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0005_auto_20150109_1605'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storypointer',
            options={'ordering': ('-pub_date',)},
        ),
    ]
