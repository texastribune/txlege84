from django.core.management.base import BaseCommand

from legislators.models import Party


class Command(BaseCommand):
    help = u'Bootstrap the Party model data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(u'Bootstrapping parties...')

        self.load_party(u'Republican')
        self.load_party(u'Democratic')

    def load_party(self, name):
        party, created = Party.objects.get_or_create(
            name=name)

        if created:
            self.stdout.write('Successfully created `{}`.'.format(name))
        else:
            self.stderr.write('We tried to create `{}`, but we found it '
                              'in the database! You sure you '
                              'wanted to do this?'.format(name))
