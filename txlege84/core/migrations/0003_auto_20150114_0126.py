# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_convenetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convenetime',
            name='chamber',
            field=models.OneToOneField(related_name='time_for', to='legislators.Chamber'),
            preserve_default=True,
        ),
    ]
