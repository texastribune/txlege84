# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0002_auto_20141120_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('openstates_id', models.CharField(max_length=9)),
                ('chamber', models.ForeignKey(related_name='committees', to='legislators.Chamber')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=20)),
                ('committee', models.ForeignKey(related_name='memberships', to='committees.Committee')),
                ('legislator', models.ForeignKey(related_name='memberships', to='legislators.Legislator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='committee',
            name='members',
            field=models.ManyToManyField(to='legislators.Legislator', through='committees.Membership'),
            preserve_default=True,
        ),
    ]
