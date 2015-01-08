# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_subject_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='became_law',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='first_action_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='last_action_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='passed_house',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='passed_senate',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
