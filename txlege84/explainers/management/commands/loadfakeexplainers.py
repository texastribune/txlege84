from faker import Factory

from django.core.management.base import BaseCommand

from explainers.models import Explainer

FAKE = Factory.create()


class Command(BaseCommand):
    help = u'Load fake explainers into the database. For development ONLY.'

    def handle(self, *args, **kwargs):
        self.load_fake_explainers()

    def load_fake_explainers(self):
        self.stdout.write(u'Loading fake explainers...')

        fakes = [{
            'title': u'What Really Happens During the 5 Months of Session',
            'status': u'P',
            'youtube_id': 'UJlA6_Ij4Pw',
            'text': FAKE.paragraph(),
            }, {
            'title': u'What is a Point of Order?',
            'status': u'P',
            'youtube_id': 'UJlA6_Ij4Pw',
            'text': FAKE.paragraph(),
            }, {
            'title': u'What Does the Lieutenant Governor do?',
            'status': u'D',
            'youtube_id': 'UJlA6_Ij4Pw',
            'text': FAKE.paragraph(),
            }, {
            'title': u'What is a Second Reading?',
            'status': u'P',
            'youtube_id': 'UJlA6_Ij4Pw',
            'text': FAKE.paragraph(),
            },
        ]

        for idx, fake in enumerate(fakes):
            self.create_explainer(fake, idx)

    def create_explainer(self, data, order):
        explainer, _ = Explainer.objects.get_or_create(
            name=data['title'],
            youtube_id=data['youtube_id'],
            text=data['text'],
            status=data['status'],
            order=order,
        )
