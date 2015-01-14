# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0006_auto_20150114_0040'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConveneTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_string', models.CharField(max_length=100)),
                ('chamber', models.OneToOneField(to='legislators.Chamber')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
