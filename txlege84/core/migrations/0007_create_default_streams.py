# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_default_streams(apps, schema_editor):
    Chamber = apps.get_model('legislators', 'Chamber')
    Stream = apps.get_model('core', 'Stream')

    Stream.objects.create(
        chamber=Chamber.objects.get(name='Texas House'),
        granicus_subdomain='tlchouse',
        camera_id=3,
        direct_event_feed=False,
    )

    Stream.objects.create(
        chamber=Chamber.objects.get(name='Texas Senate'),
        granicus_subdomain='tlcsenate',
        camera_id=8,
        direct_event_feed=False,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_stream'),
    ]

    operations = [
        migrations.RunPython(add_default_streams),
    ]
