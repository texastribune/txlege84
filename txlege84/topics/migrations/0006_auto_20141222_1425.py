# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0005_auto_20141222_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='active',
        ),
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.CharField(default='D', max_length=1, choices=[('D', 'Draft'), ('P', 'Published'), ('W', 'Withdrawn')]),
            preserve_default=True,
        ),
    ]
