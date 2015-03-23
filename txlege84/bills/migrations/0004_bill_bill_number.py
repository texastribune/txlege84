# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0003_remove_bill_sponsors'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='bill_number',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
