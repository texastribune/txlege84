# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_auto_20150323_1715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'ordering': ('chamber__name', 'bill_type', 'bill_number')},
        ),
    ]
