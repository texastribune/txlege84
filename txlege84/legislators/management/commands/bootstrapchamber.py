from django.core.management.base import BaseCommand

from legislators.models import Chamber


class Command(BaseCommand):
    help = u'Bootstrap the Chamber model data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(u'Bootstrapping chambers...')

        self.load_chamber(u'Texas Senate')
        self.load_chamber(u'Texas House')

    def load_chamber(self, name):
        chamber, created = Chamber.objects.get_or_create(
            name=name)

        if created:
            self.stdout.write('Successfully created `{}`.'.format(name))
        else:
            self.stderr.write('We tried to create `{}`, but we found it '
                              'in the database! You sure you '
                              'wanted to do this?'.format(name))
