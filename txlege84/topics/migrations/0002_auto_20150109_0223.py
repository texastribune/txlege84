# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuetext',
            name='issue',
            field=models.ForeignKey(related_name='texts', blank=True, to='topics.Issue', null=True),
            preserve_default=True,
        ),
    ]
