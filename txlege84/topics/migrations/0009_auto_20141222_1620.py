# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0008_topic_curators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='active_text',
            field=models.OneToOneField(null=True, blank=True, to='topics.IssueText'),
            preserve_default=True,
        ),
    ]
