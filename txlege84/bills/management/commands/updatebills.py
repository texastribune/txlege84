from datetime import datetime, timedelta
from optparse import make_option

from django.core.management.base import BaseCommand

from bills.models import Action, Bill, Sponsorship, Subject
from committees.models import Committee
from legislators.models import Legislator

from sunlight import openstates


class Command(BaseCommand):
    help = u'Partially load bills into the database.'

    custom_options = (
        make_option(
            '-b',
            '--bulk',
            action='store_true',
            dest='bulk',
            default=False,
            help='Load all bills since the last bulk update.'
        ),
        make_option(
            '-y',
            '--yesterday',
            action='store_true',
            dest='yesterday',
            default=False,
            help='Load all bills since yesterday.'
        ),

    )

    option_list = BaseCommand.option_list + custom_options

    def handle(self, *args, **kwargs):
        if kwargs['bulk']:
            self.latest_date = self.get_latest_download_date()
        elif kwargs['yesterday']:
            yesterday = datetime.now() - timedelta(days=1)
            self.latest_date = yesterday.date().isoformat()
        else:
            self.stderr.write('A time frame must '
                              'be provided! (--bulk or --yesterday)')
            return

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
        print self.latest_date
        return openstates.bills(
            state='tx',
            updated_since=self.latest_date,
            search_window='session')

    def get_bill_data(self, bill_name):
        return openstates.bill_detail('tx', '84', bill_name)

    def load_bills(self):
        for bill_data in self.get_updated_bill_list():
            self.load_bill(bill_data)

    def load_bill(self, data):
        self.stdout.write(u'Loading {}...'.format(data['bill_id']))

        # Creates the bill
        bill, created = Bill.objects.update_or_create(
            name=data['bill_id'],
            openstates_id=data['id'],
            defaults={
                'description': data['title'],
                'bill_type': data['type'][0].lower(),
                'chamber': (self.senate_chamber if data['chamber'] == 'upper'
                            else self.house_chamber),
            }
        )

        # Sets the bill's subjects
        bill.subjects = [Subject.objects.get(name=subject)
                         for subject in data['subjects']]

        # Drop non-existent sponsors
        lege_ids = [i['leg_id'] for i in data['sponsors'] if i['leg_id']]

        missing_sponsorships = bill.sponsorships.exclude(
            legislator__openstates_id__in=lege_ids)

        for sponsorship in missing_sponsorships:
            sponsorship.delete()

        # Add or update remaining sponsors
        for member in data['sponsors']:
            if not member['leg_id']:
                continue

            legislator = Legislator.objects.get(
                openstates_id=member['leg_id']
            )

            Sponsorship.objects.update_or_create(
                legislator=legislator,
                bill=bill,
                defaults={
                    'role': member['type'].lower()
                },
            )

        # Adds or updates actions
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

            Action.objects.update_or_create(
                number=action['+action_number'],
                bill=bill,
                defaults={
                    'text': action['action'],
                    'date': action['date'].split(' ')[0],
                    'acting_chamber': (self.senate_chamber
                                       if action['actor'] == 'upper'
                                       else self.house_chamber),
                    'related_committee': related_committee,
                },
            )
