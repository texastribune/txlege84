# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20150109_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='active_text',
            field=models.ForeignKey(related_name='issues', blank=True, to='topics.IssueText', null=True),
            preserve_default=True,
        ),
    ]
