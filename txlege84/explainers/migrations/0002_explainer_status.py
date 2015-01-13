# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explainers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='explainer',
            name='status',
            field=models.CharField(default='D', max_length=1, choices=[('D', 'Draft'), ('P', 'Published'), ('W', 'Withdrawn')]),
            preserve_default=True,
        ),
    ]
