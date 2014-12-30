# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0003_auto_20141205_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.SlugField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
