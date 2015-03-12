from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import ConveneTime
from legislators.models import Chamber

from dateutil.parser import parse
import requests


class Command(BaseCommand):
    help = u'Scrape TLO for convening times.'

    def handle(self, *args, **kwargs):
        self.update_time('House')
        self.update_time('Senate')

    def update_time(self, chamber):
        self.stdout.write(u'Updating {} convening time...'.format(chamber))

        page = requests.get('http://www.capitol.state.tx.us/tlodocs'
                            '/SessionTime/{}SessTime.js'.format(chamber))

        time_string = page.text.strip()[16:-3]
        status, time = time_string.split(' until ')
        time = timezone.make_aware(
            parse(time.replace(' noon', '')), timezone.get_default_timezone())

        chamber_model = Chamber.objects.get(name='Texas {}'.format(chamber))
        convene_time = ConveneTime.objects.get(chamber=chamber_model)

        if convene_time.time_string == time_string:
            self.stdout.write('Has not changed.')
            return

        convene_time.time_string = time_string
        convene_time.status = status
        convene_time.time = time
        convene_time.active = True

        convene_time.save()

        self.stdout.write(u'Now set to: {}'.format(time_string))
