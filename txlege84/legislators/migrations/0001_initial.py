# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chamber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=12)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Legislator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=40)),
                ('middle_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('district', models.IntegerField(null=True, blank=True)),
                ('profile_url', models.URLField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('openstates_id', models.CharField(unique=True, max_length=9)),
                ('chamber', models.ForeignKey(related_name='legislators', blank=True, to='legislators.Chamber', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='legislator',
            name='party',
            field=models.ForeignKey(related_name='legislators', blank=True, to='legislators.Party', null=True),
            preserve_default=True,
        ),
    ]
