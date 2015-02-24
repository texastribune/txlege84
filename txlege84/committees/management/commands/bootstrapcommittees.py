from django.core.management.base import BaseCommand

from committees.models import Committee, Membership
from legislators.models import Chamber, Legislator

from sunlight import openstates


class Command(BaseCommand):
    help = u'Bootstrap the Committee model data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(u'Bootstrapping committees...')

        self.load_committees()

    def load_committees(self):
        committee_list = openstates.committees(state='tx')

        for committee in committee_list:
            self.load_committee(committee)

    def load_committee(self, obj):
        data = openstates.committee_detail(obj['id'])
        committee_name = data['committee']

        if committee_name == 'Committee of the Whole Senate':
            self.stdout.write(u'Skipping {}.'.format(committee_name))
            return

        self.stdout.write(u'Loading {}...'.format(committee_name))

        chamber = Chamber.objects.get(
            name=u'Texas Senate' if data['chamber'] == 'upper'
            else u'Texas House'
        )

        committee, _ = Committee.objects.get_or_create(
            name=committee_name,
            chamber=chamber,
            openstates_id=data['id'],
        )

        committee.members.clear()

        member_list = []

        for member in data['members']:
            legislator = Legislator.objects.get(openstates_id=member['leg_id'])

            member = Membership(
                legislator=legislator,
                committee=committee,
                role=member['role'].title(),
            )

            member_list.append(member)

        Membership.objects.bulk_create(member_list)
