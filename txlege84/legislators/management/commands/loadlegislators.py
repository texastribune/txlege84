from datetime import datetime
from glob import glob
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from legislators.models import Chamber, Legislator, Party


class Command(BaseCommand):
    help = u'Bulk load the legislator data into the database.'

    def handle(self, *args, **kwargs):
        self.load_legislators()

    def date_converter(self, date_string):
        if date_string:
            return datetime.strptime(date_string, '%m/%d/%Y').date()
        else:
            return None

    def load_legislators(self):
        self.stdout.write(u'Loading legislators...')

        legislator_files = glob('{}/legislators/TXL*'.format(
                                settings.DOWNLOAD_DIR))

        for path in legislator_files:
            with open(path, 'rb') as f:
                data = json.loads(f.read())

                # if they have roles, they're active
                if data['roles']:
                    primary_role = data['roles'][0]
                elif '83' in data['old_roles']:
                    primary_role = data['old_roles']['83'][0]
                else:
                    continue

                self.stdout.write(u'Loading {0} {1}...'.format(
                    data['first_name'],
                    data['last_name']))

                party, _ = Party.objects.get_or_create(
                    name=primary_role['party'])

                if 'chamber' in primary_role:
                    chamber, _ = Chamber.objects.get_or_create(
                        name=u'Texas Senate' if primary_role['chamber']
                             == 'upper' else u'Texas House'
                    )
                else:
                    chamber = None

                if 'district' in primary_role:
                    district = int(primary_role['district'])
                else:
                    district = None

                Legislator.objects.get_or_create(
                    first_name=data['first_name'],
                    middle_name=data['middle_name'],
                    last_name=data['last_name'],
                    party=party,
                    chamber=chamber,
                    district=district,
                    profile_url=data['url'],
                    openstates_id=data['leg_id'],
                )
