# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def parse_numbers(apps, schema_editor):
    Bill = apps.get_model('bills', 'Bill')
    for bill in Bill.objects.all():
        bill_number_text = bill.name.split(' ')[1]
        bill_number = int(bill_number_text)

        bill.bill_number = bill_number
        bill.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_bill_bill_number'),
    ]

    operations = [
        migrations.RunPython(parse_numbers),
    ]
