from django.core.management.base import BaseCommand

from bills.models import Subject


class Command(BaseCommand):
    help = u'Bootstrap the Subject model data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(u'Bootstrapping bill subjects...')
        self.load_subjects()

    def load_subjects(self):
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
            self.load_subject(subject)

    def load_subject(self, name):
        subject, created = Subject.objects.get_or_create(
            name=name)

        if created:
            self.stdout.write('Successfully created `{}`.'.format(name))
        else:
            self.stderr.write('We tried to create `{}`, but we found it '
                              'in the database! You sure you '
                              'wanted to do this?'.format(name))
