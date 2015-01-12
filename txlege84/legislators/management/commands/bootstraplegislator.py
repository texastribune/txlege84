from csv import DictReader

import requests

from django.core.management.base import BaseCommand

from legislators.models import Chamber, Legislator, Party

from sunlight import openstates


class Command(BaseCommand):
    help = u'Bootstrap the Legislator model data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(u'Bootstrapping legislators...')

        self.fetch_tribune_match()
        self.load_legislators()

    def fetch_tribune_match(self):
        url = ('https://docs.google.com/a/texastribune.org'
               '/spreadsheets/d/1dsyAm2XZLW5yHw3U8fSn8aZupyB8547uhqdgQGKQgUM/'
               'export?format=csv&id='
               '1dsyAm2XZLW5yHw3U8fSn8aZupyB8547uhqdgQGKQgUM&gid=1667065091')

        raw_csv = requests.get(url)
        reader = DictReader(raw_csv.iter_lines())
        self.tribune_match = {i['openstates_id']: i for i in reader}

    def load_legislators(self):
        legislator_list = openstates.legislators(state='tx')

        for lawmaker in legislator_list:
            self.load_legislator(lawmaker)

    def load_legislator(self, lawmaker):
        data = openstates.legislator_detail(lawmaker['id'])

        self.stdout.write(u'Loading {0} {1}...'.format(
            data['first_name'], data['last_name']))

        if 'party' in data:
            party = Party.objects.get(name=data['party'])
        else:
            party = None

        if 'chamber' in data:
            chamber = Chamber.objects.get(
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

        if 'offices' in data:
            for entry in data['offices']:
                if entry['type'] == 'capitol':
                    capitol_office = entry
                    break
            else:
                capitol_office = None

            for entry in data['offices']:
                if entry['type'] == 'district':
                    district_office = entry
                    break
            else:
                district_office = None

            if capitol_office:
                capitol_address = capitol_office['address']
                capitol_phone = capitol_office['phone']
                if capitol_phone:
                    capitol_phone = capitol_phone.replace('(', '')
                    capitol_phone = capitol_phone.replace(') ', '-')
            else:
                capitol_address = None
                capitol_phone = None

            if district_office:
                district_address = district_office['address']
                district_phone = district_office['phone']
                if district_phone:
                    district_phone = district_phone.replace('(', '')
                    district_phone = district_phone.replace(') ', '-')
            else:
                district_address = None
                district_phone = None

            if data['id'] in self.tribune_match:
                match = self.tribune_match[data['id']]

                tribune_city = match['city']
                tribune_slug = match['slug']
                tribune_photo = match['photo']
            else:
                tribune_city = None
                tribune_slug = None
                tribune_photo = None

            legislator, created = Legislator.objects.get_or_create(
                first_name=data['first_name'],
                middle_name=data['middle_name'],
                last_name=data['last_name'],
                party=party,
                chamber=chamber,
                district=district,
                profile_url=profile_url,
                active=data['active'],
                capitol_address=capitol_address,
                capitol_phone=capitol_phone,
                district_address=district_address,
                district_phone=district_phone,
                openstates_id=data['leg_id'],
                tribune_city=tribune_city,
                tribune_slug=tribune_slug,
                tribune_photo=tribune_photo,
            )

            name = data['full_name']

            if created:
                self.stdout.write(u'Successfully created `{}`.'.format(name))
            else:
                self.stderr.write(u'We tried to create `{}`, but we found it '
                                  'in the database! You sure you '
                                  'wanted to do this?'.format(name))
