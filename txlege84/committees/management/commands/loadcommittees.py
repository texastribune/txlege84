from datetime import datetime
from glob import glob
import json
# from optparse import make_option
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from committees.models import Committee, Membership
from legislators.models import Chamber, Legislator


class Command(BaseCommand):
    help = u'Bulk load the committee data into the database.'

    # custom_options = (
    #     make_option(
    #         '-s',
    #         '--since',
    #         action='store',
    #         dest='since',
    #         default=None,
    #         help='Load all filings since this date ("2013-07-01")'
    #     ),
    # )

    # option_list = BaseCommand.option_list + custom_options

    def handle(self, *args, **kwargs):
        self.load_committees()

    def date_converter(self, date_string):
        if date_string:
            return datetime.strptime(date_string, '%m/%d/%Y').date()
        else:
            return None

    def load_committees(self):
        self.stdout.write(u'Loading committees...')

        committee_files = glob('{}/committees/TXC*'.format(
                               settings.DOWNLOAD_DIR))

        for path in committee_files:
            with open(path, 'rb') as f:
                data = json.loads(f.read())

                self.stdout.write(u'Loading {}...'.format(data['committee']))

                chamber = Chamber.objects.get(
                    name=(u'Texas Senate' if data['chamber'] == 'upper'
                          else u'Texas House')
                )

                committee, created = Committee.objects.get_or_create(
                    name=data['committee'],
                    chamber=chamber,
                    openstates_id=data['id']
                )

                if created:
                    for member in data['members']:
                        legislator = Legislator.objects.get(
                            openstates_id=member['leg_id']
                        )

                        Membership.objects.create(
                            legislator=legislator,
                            committee=committee,
                            role=member['role'].title()
                        )
