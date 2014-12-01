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

                self.stdout.write(u'Loading {0} {1}...'.format(
                    data['first_name'],
                    data['last_name']))

                if 'party' in data:
                    party, _ = Party.objects.get_or_create(
                        name=data['party'])
                else:
                    party = None

                if 'chamber' in data:
                    chamber, _ = Chamber.objects.get_or_create(
                        name=u'Texas Senate' if data['chamber'] == 'upper'
                        else u'Texas House'
                    )
                else:
                    chamber = None

                if 'district' in data:
                    if data['district']:
                        district = int(data['district'])
                    else:
                        district = None
                else:
                    district = None

                if 'url' in data:
                    profile_url = data['url']
                else:
                    profile_url = None

                Legislator.objects.get_or_create(
                    first_name=data['first_name'],
                    middle_name=data['middle_name'],
                    last_name=data['last_name'],
                    party=party,
                    chamber=chamber,
                    district=district,
                    profile_url=profile_url,
                    active=data['active'],
                    openstates_id=data['leg_id'],
                )
