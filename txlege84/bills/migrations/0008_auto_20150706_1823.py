# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0007_bill_vetoed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsorship',
            options={'ordering': ['ordering']},
        ),
        migrations.AddField(
            model_name='sponsorship',
            name='ordering',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
