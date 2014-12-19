# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_bill_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ['date', 'pk']},
        ),
    ]
