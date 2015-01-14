from django.core.management.base import BaseCommand

from core.models import ConveneTime
from legislators.models import Chamber

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

        ConveneTime.objects.update_or_create(
            chamber=Chamber.objects.get(name='Texas {}'.format(chamber)),
            time_string=time_string,
        )

        self.stdout.write(u'Now set to: {}'.format(time_string))
