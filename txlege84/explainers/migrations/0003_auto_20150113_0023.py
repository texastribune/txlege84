# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explainers', '0002_explainer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explainer',
            name='name',
            field=models.CharField(max_length=200, verbose_name='title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='explainer',
            name='youtube_id',
            field=models.CharField(max_length=11, verbose_name='YouTube ID'),
            preserve_default=True,
        ),
    ]
