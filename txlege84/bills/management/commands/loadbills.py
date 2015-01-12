from glob import glob
import json

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bills.models import Action, Bill, Subject, Sponsorship
from committees.models import Committee
from legislators.models import Chamber, Legislator

from sunlight import openstates


class Command(BaseCommand):
    help = u'Load bill data from Open States.'

    custom_options = (
        make_option(
            '--from-bulk',
            action='store_true',
            dest='from_bulk',
            default=None,
            help=('Use the bulk download from Open States to mass load '
                  'bills. Expects a --session to be passed.')
        ),
        make_option(
            '--session',
            action='store',
            dest='session',
            default=None,
            help=('The session to target for bill loading. Required if '
                  '--from-bulk is being used. Otherwise, the default is '
                  'the current session.')
        ),
        make_option(
            '--since',
            action='store',
            dest='since',
            default=None,
            help='Only seek out bills that have been updated since this date.'
        )
    )

    option_list = BaseCommand.option_list + custom_options

    def handle(self, *args, **kwargs):
        # Cache for bill/action loading
        self.senate_chamber = Chamber.objects.get(name='Texas Senate')
        self.house_chamber = Chamber.objects.get(name='Texas House')

        if kwargs['from_bulk']:
            if not kwargs['session']:
                raise CommandError('--session must be set when '
                                   'using --from-bulk!')

            self.bulk_load_bills(kwargs['session'])
        else:
            self.load_bills(kwargs['session'], kwargs['since'])

    def get_latest_download_date(self):
        latest_date = openstates.state_metadata('tx')
        return latest_date['latest_json_date'].split(' ')[0]

    def bulk_load_bills(self, session):
        # Loading Texas Senate bills
        self.bulk_load_chamber(session, 'upper', 'S')

        # Loading Texas House bills
        self.bulk_load_chamber(session, 'lower', 'H')

        self.load_bills_since(self.get_latest_download_date)

    def bulk_load_chamber(self, session, chamber, abbr):
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

    def load_bills(self, session, date):
        search_kwargs = {
            'state': 'tx',
            'search_window': ('session:{}'.format(session)
                              if session else 'session'),
            'page': 1,
            'per_page': 10000,
        }

        if date:
            search_kwargs['updated_since'] = date

        while True:
            bills = openstates.bills(**search_kwargs)

            for bill in bills:
                bill_data = self.fetch_bill(bill['id'])
                self.load_bill(bill_data)

            search_kwargs['page'] += 1

            if len(bills) < 10000:
                break

    def fetch_bill(self, openstates_id):
        return openstates.bill(openstates_id)

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

        # Creates or updates the bill
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
                    try:
                        related_committee = Committee.objects.get(
                            openstates_id=related_entity_id)
                    except Committee.DoesNotExist:
                        self.stderr.write('No Committee found for `{}`'.format(
                            related_entity_name))
                elif (related_entity_name ==
                      'Vet Affairs & Military Installations'):
                    try:
                        related_committee = Committee.objects.get(
                            openstates_id='TXC000030')
                    except Committee.DoesNotExist:
                        self.stderr.write('No Committee found for `{}`'.format(
                            related_entity_name))
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
