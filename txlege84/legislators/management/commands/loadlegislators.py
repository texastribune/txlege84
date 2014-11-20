from datetime import datetime
from glob import glob
import json
# from optparse import make_option
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from legislators.models import Chamber, Legislator, Party


class Command(BaseCommand):
    help = u'Bulk load the legislator data into the database.'

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
                if not data['roles']:
                    continue

                self.stdout.write(u'Loading {0} {1}...'.format(
                    data['first_name'],
                    data['last_name']))

                party, _ = Party.objects.get_or_create(name=data['party'])

                if data['chamber']:
                    chamber, _ = Chamber.objects.get_or_create(
                        name=u'Texas Senate' if data['chamber'] == 'upper'
                             else u'Texas House')
                else:
                    chamber = None

                primary_role = data['roles'][0]

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

        # with open(filer_csv_path, 'rb') as f:
        #     reader = csv.DictReader(f)

        #     for entry in reader:
        #         entry_treasurer_start_date = self.date_converter(
        #             entry['TRES_START'])
        #         try:
        #             filer = Filer.objects.get(id=entry['FILER_ID'])
        #             treasurer_start_date = filer.treasure_start_date

        #             if (not entry_treasurer_start_date
        #                     or not treasurer_start_date):
        #                 continue

        #             if entry_treasurer_start_date > treasurer_start_date:
        #                 Filer.objects.filter(id=entry['FILER_ID']).update(
        #                     filer_type=entry['FILER_TYPE'],
        #                     filer_status=entry['PAFLSTAT'],
        #                     first_name=entry['FILER_NAMF'],
        #                     last_name=entry['FILER_NAML'],
        #                     prefix=entry['FILER_NAMT'],
        #                     suffix=entry['FILER_NAMS'],
        #                     nickname=entry['FILERSHORT'],
        #                     address_1=entry['FILER_ADR1'],
        #                     address_2=entry['FILER_ADR2'],
        #                     city=entry['FILER_CITY'],
        #                     state=entry['FILER_STCD'],
        #                     zip_code=entry['FILER_ZIP4'],
        #                     mailing_address_1=entry['FMAIL_ADR1'],
        #                     mailing_address_2=entry['FMAIL_ADR2'],
        #                     mailing_city=entry['FMAIL_CITY'],
        #                     mailing_state=entry['FMAIL_STCD'],
        #                     mailing_zip_code=entry['FMAIL_ZIP4'],
        #                     phone=entry['FILER_PHON'],
        #                     phone_extension=entry['FILER_PH_X'],
        #                     sought_office_type=entry['BALLOT_TYP'],
        #                     sought_office_district=entry['BALLOT_DST'],
        #                     sought_office_place=entry['BALLOT_PLC'],
        #                     sought_office_county=entry['BALLOT_CO'],
        #                     party=entry['POL_PARTY'],
        #                     treasure_start_date=entry_treasurer_start_date
        #                 )

        #         except Filer.DoesNotExist:
        #             Filer.objects.create(
        #                 id=entry['FILER_ID'],
        #                 filer_type=entry['FILER_TYPE'],
        #                 filer_status=entry['PAFLSTAT'],
        #                 first_name=entry['FILER_NAMF'],
        #                 last_name=entry['FILER_NAML'],
        #                 prefix=entry['FILER_NAMT'],
        #                 suffix=entry['FILER_NAMS'],
        #                 nickname=entry['FILERSHORT'],
        #                 address_1=entry['FILER_ADR1'],
        #                 address_2=entry['FILER_ADR2'],
        #                 city=entry['FILER_CITY'],
        #                 state=entry['FILER_STCD'],
        #                 zip_code=entry['FILER_ZIP4'],
        #                 mailing_address_1=entry['FMAIL_ADR1'],
        #                 mailing_address_2=entry['FMAIL_ADR2'],
        #                 mailing_city=entry['FMAIL_CITY'],
        #                 mailing_state=entry['FMAIL_STCD'],
        #                 mailing_zip_code=entry['FMAIL_ZIP4'],
        #                 phone=entry['FILER_PHON'],
        #                 phone_extension=entry['FILER_PH_X'],
        #                 sought_office_type=entry['BALLOT_TYP'],
        #                 sought_office_district=entry['BALLOT_DST'],
        #                 sought_office_place=entry['BALLOT_PLC'],
        #                 sought_office_county=entry['BALLOT_CO'],
        #                 party=entry['POL_PARTY'],
        #                 treasure_start_date=entry_treasurer_start_date
        #             )
