from datetime import datetime
from glob import glob
import json
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from bills.models import Action, Bill, Sponsorship, Subject
from committees.models import Committee
from legislators.models import Chamber, Legislator


class Command(BaseCommand):
    help = u'Bulk load the legislator data into the database.'

    custom_options = (
        make_option(
            '-s',
            '--session',
            action='store',
            dest='session',
            default=None,
            help='Load bills from a particular session.'
        ),
    )

    option_list = BaseCommand.option_list + custom_options

    def handle(self, *args, **kwargs):
        self.load_subjects()

        # Cache for bill/action loading
        self.senate_chamber = Chamber.objects.get(name='Texas Senate')
        self.house_chamber = Chamber.objects.get(name='Texas House')

        if not kwargs['session']:
            self.stderr.write('--session is required!')

        # Loading Texas Senate bills
        self.load_bills(kwargs['session'], 'upper', 'S')

        # Loading Texas House bills
        self.load_bills(kwargs['session'], 'lower', 'H')

    def date_converter(self, date_string):
        if date_string:
            return datetime.strptime(date_string, '%m/%d/%Y').date()
        else:
            return None

    def load_subjects(self):
        self.stdout.write(u'Loading bill subjects...')

        subjects = [
            u'Agriculture and Food',
            u'Animal Rights and Wildlife Issues',
            u'Arts and Humanities',
            u'Budget, Spending, and Taxes',
            u'Business and Consumers',
            u'Campaign Finance and Election Issues',
            u'Civil Liberties and Civil Rights',
            u'Commerce',
            u'Crime',
            u'Drugs',
            u'Education',
            u'Energy',
            u'Environmental',
            u'Executive Branch',
            u'Family and Children Issues',
            u'Federal, State, and Local Relations',
            u'Gambling and Gaming',
            u'Government Reform',
            u'Guns',
            u'Health',
            u'Housing and Property',
            u'Immigration',
            u'Indigenous Peoples',
            u'Insurance',
            u'Judiciary',
            u'Labor and Employment',
            u'Legal Issues',
            u'Legislative Affairs',
            u'Military',
            u'Municipal and County Issues',
            u'Nominations',
            u'Other',
            u'Public Services',
            u'Recreation',
            u'Reproductive Issues',
            u'Resolutions',
            u'Science and Medical Research',
            u'Senior Issues',
            u'Sexual Orientation and Gender Issues',
            u'Social Issues',
            u'State Agencies',
            u'Technology and Communication',
            u'Trade',
            u'Transportation',
            u'Welfare and Poverty',
        ]

        for subject in subjects:
            Subject.objects.get_or_create(name=subject)

    def load_bills(self, session, chamber, abbr):
        bill_files = glob(
            '{dir}/bills/tx/{session}/{chamber}/{abbr}*'.format(
                dir=settings.DOWNLOAD_DIR,
                session=session,
                chamber=chamber,
                abbr=abbr))

        for path in bill_files:
            with open(path, 'rb') as f:
                data = json.loads(f.read())

                self.load_bill(data)

    def load_bill(self, data):
        self.stdout.write(u'Loading {}...'.format(data['bill_id']))

        first_action_date = (data['action_dates']['first'].split(' ')[0]
                             if data['action_dates']['first'] else None)
        last_action_date = (data['action_dates']['last'].split(' ')[0]
                            if data['action_dates']['last'] else None)
        passed_house = (data['action_dates']['passed_lower'].split(' ')[0]
                        if data['action_dates']['passed_lower'] else None)
        passed_senate = (data['action_dates']['passed_upper'].split(' ')[0]
                         if data['action_dates']['passed_upper'] else None)
        became_law = (data['action_dates']['signed'].split(' ')[0]
                      if data['action_dates']['signed'] else None)

        # Creates the bill
        bill, created = Bill.objects.update_or_create(
            name=data['bill_id'],
            openstates_id=data['id'],
            defaults={
                'description': data['title'],
                'bill_type': data['type'][0].lower(),
                'chamber': (self.senate_chamber if data['chamber'] == 'upper'
                            else self.house_chamber),
                'first_action_date': first_action_date,
                'last_action_date': last_action_date,
                'passed_house': passed_house,
                'passed_senate': passed_senate,
                'became_law': became_law,
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
                    'role': member['official_type'].lower()
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
