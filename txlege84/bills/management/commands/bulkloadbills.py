from datetime import datetime
from glob import glob
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from bills.models import Action, Bill, Sponsorship, Subject
from committees.models import Committee
from legislators.models import Chamber, Legislator


class Command(BaseCommand):
    help = u'Bulk load the legislator data into the database.'

    def handle(self, *args, **kwargs):
        self.load_subjects()

        # Cache for bill/action loading
        self.senate_chamber = Chamber.objects.get(name='Texas Senate')
        self.house_chamber = Chamber.objects.get(name='Texas House')

        self.load_senate()
        self.load_house()

    def date_converter(self, date_string):
        if date_string:
            return datetime.strptime(date_string, '%m/%d/%Y').date()
        else:
            return None

    def load_subjects(self):
        self.stdout.write(u'Loading bill subjects...')

        subjects = [
            'Agriculture and Food',
            'Animal Rights and Wildlife Issues',
            'Arts and Humanities',
            'Budget, Spending, and Taxes',
            'Business and Consumers',
            'Campaign Finance and Election Issues',
            'Civil Liberties and Civil Rights',
            'Commerce',
            'Crime',
            'Drugs',
            'Education',
            'Energy',
            'Environmental',
            'Executive Branch',
            'Family and Children Issues',
            'Federal, State, and Local Relations',
            'Gambling and Gaming',
            'Government Reform',
            'Guns',
            'Health',
            'Housing and Property',
            'Immigration',
            'Indigenous Peoples',
            'Insurance',
            'Judiciary',
            'Labor and Employment',
            'Legal Issues',
            'Legislative Affairs',
            'Military',
            'Municipal and County Issues',
            'Nominations',
            'Other',
            'Public Services',
            'Recreation',
            'Reproductive Issues',
            'Resolutions',
            'Science and Medical Research',
            'Senior Issues',
            'Sexual Orientation and Gender Issues',
            'Social Issues',
            'State Agencies',
            'Technology and Communication',
            'Trade',
            'Transportation',
            'Welfare and Poverty',
        ]

        for subject in subjects:
            Subject.objects.get_or_create(name=subject)

    def load_senate(self):
        self.stdout.write(u'Loading Senate bills...')

        senate_bill_files = glob('{}/bills/tx/83/upper/S*'.format(
            settings.DOWNLOAD_DIR))

        for path in senate_bill_files:
            with open(path, 'rb') as f:
                data = json.loads(f.read())

                self.load_bill(data)

    def load_house(self):
        self.stdout.write(u'Loading House bills...')

        house_bill_files = glob('{}/bills/tx/83/lower/H*'.format(
            settings.DOWNLOAD_DIR))

        for path in house_bill_files:
            with open(path, 'rb') as f:
                data = json.loads(f.read())

                self.load_bill(data)

    def load_bill(self, data):
        self.stdout.write(u'Loading {}...'.format(data['bill_id']))

        bill, _ = Bill.objects.get_or_create(
            name=data['bill_id'],
            description=data['title'],
            bill_type=data['type'][0].title(),
            chamber=(self.senate_chamber if data['chamber'] == 'upper'
                     else self.house_chamber),
            openstates_id=data['id']
        )

        for subject in data['subjects']:
            bill.subjects.add(Subject.objects.get(name=subject))

        for member in data['sponsors']:
            if not member['leg_id']:
                continue

            legislator = Legislator.objects.get(
                openstates_id=member['leg_id']
            )

            Sponsorship.objects.get_or_create(
                legislator=legislator,
                bill=bill,
                role=member['type'].title()
            )

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

            Action.objects.get_or_create(
                number=action['+action_number'],
                text=action['action'],
                date=action['date'].split(' ')[0],
                acting_chamber=(self.senate_chamber
                                if action['actor'] == 'upper'
                                else self.house_chamber),
                related_committee=related_committee,
                bill=bill
            )
