# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0007_auto_20150311_1607'),
        ('core', '0005_convenetime_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('granicus_subdomain', models.CharField(help_text=b'Granicus subdomain for stream', max_length=20)),
                ('camera_id', models.IntegerField(help_text=b'Identifier for direct camera stream')),
                ('direct_event_feed', models.BooleanField(default=False, help_text=b'Use an event feed instead of a camera feed')),
                ('feed_id', models.IntegerField(help_text=b'Feed identifier for direct embed', null=True, blank=True)),
                ('event_id', models.IntegerField(help_text=b'Event identifier for direct embed', null=True, blank=True)),
                ('chamber', models.OneToOneField(related_name='stream_for', to='legislators.Chamber', help_text=b'Chamber viewable in stream')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
