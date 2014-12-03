# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0001_initial'),
        ('committees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=4)),
                ('text', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('acting_chamber', models.ForeignKey(related_name='actions', to='legislators.Chamber')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('openstates_id', models.CharField(unique=True, max_length=11)),
                ('bill_type', models.CharField(max_length=21)),
                ('chamber', models.ForeignKey(related_name='bills', to='legislators.Chamber')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=20)),
                ('bill', models.ForeignKey(related_name='sponsorships', to='bills.Bill')),
                ('legislator', models.ForeignKey(related_name='sponsorships', to='legislators.Legislator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bill',
            name='sponsors',
            field=models.ManyToManyField(to='legislators.Legislator', through='bills.Sponsorship'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='subjects',
            field=models.ManyToManyField(related_name='bills', to='bills.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='bill',
            field=models.ForeignKey(related_name='actions', to='bills.Bill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='related_committee',
            field=models.ForeignKey(related_name='actions', blank=True, to='committees.Committee', null=True),
            preserve_default=True,
        ),
    ]
