# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0004_issue_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='photo',
            new_name='image',
        ),
    ]
