from datetime import datetime
from glob import glob
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from bills.models import Action, Bill, Sponsorship, Subject
from committees.models import Committee
from legislators.models import Chamber, Legislator

from sunlight import openstates


class Command(BaseCommand):
    help = u'Bulk load the legislator data into the database.'

    def handle(self, *args, **kwargs):
        self.latest_date = self.get_latest_download_date()
        self.bill_list = self.get_updated_bill_list()

        self.load_bills()

    def date_converter(self, date_string):
        if date_string:
            return datetime.strptime(date_string, '%m/%d/%Y').date()
        else:
            return None

    def get_latest_download_date(self):
        latest_date = openstates.state_metadata('tx')
        return latest_date['latest_json_date'].split(' ')[0]

    def get_updated_bill_list(self):
        return openstates.bills(
            state='tx',
            updated_since=self.latest_date,
            search_window='session',)

    def get_bill_data(self, bill_name):
        return openstates.bill_detail('tx', '84', bill_name)

    def load_bills(self):
        for bill_data in self.bill_list:
            bill_name = bill_data['bill_id']

            try:
                bill = Bill.objects.get(openstates_id=bill_data['id'])
                self.update_bill(bill_name, bill)
            except Bill.DoesNotExist:
                self.add_bill(bill_name)

    def update_bill(self, bill_name, bill):
        data = self.get_bill_data(bill_name)

        for action in data['actions']:

            if action['related_entities']:
                related_entity_name = action['related_entities'][0]['name']
                related_entity_id = action['related_entities'][0]['id']

                if related_entity_id:
                    related_committee = Committee.objects.get(
                        openstates_id=related_entity_id)
                elif (related_entity_name ==
                      'Vet Affairs & Military Installations'):
                    related_committee = Committee.objects.get(
                        openstates_id='TXC000030')
            else:
                related_committee = None

            updated_values = {
                'text': action['action'],
                'date': action['date'].split(' ')[0],
                'acting_chamber': (self.senate_chamber
                                   if action['actor'] == 'upper'
                                   else self.house_chamber),
                'related_committee': related_committee,
            }

            Action.objects.update_or_create(
                number=action['+action_number'],
                bill=bill,
                defaults=updated_values,
            )

    def add_bill(self, bill_name):
        print bill_name
