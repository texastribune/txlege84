# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0007_auto_20150311_1607'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('name',)},
        ),
    ]
