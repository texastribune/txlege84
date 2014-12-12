from sets import Set

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from legislators.models import Legislator


class Command(BaseCommand):
    help = u'Check Legislator url\'s for errors.'

    def handle(self, *args, **kwargs):

        #This checks to make sure all of the legislator URL's

        slugs = [legislator.slug for legislator in Legislator.objects.all() ]
        dupes = set([slug for slug in slugs if slugs.count(slug) > 1])

        if len(dupes) == 0:
            print "Everything is OK!"
        else:
            print dupes
            print "Not so good"
            raise CommandError("Duplicate URL's in legislator_slugs")
