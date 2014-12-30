# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_issue_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='photo',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
