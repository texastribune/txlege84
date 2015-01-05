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
            'title': 'What Really Happens During the 5 Months of Session',
            'youtube_id': 'UJlA6_Ij4Pw',
            'text': FAKE.paragraph(),
            }, {
            'title': 'What is a Point of Order?',
            'youtube_id': 'UJlA6_Ij4Pw',
            'text': FAKE.paragraph(),
            }, {
            'title': 'What Does the Lieutenant Governor do?',
            'youtube_id': 'UJlA6_Ij4Pw',
            'text': FAKE.paragraph(),
            }, {
            'title': 'What is a Second Reading?',
            'youtube_id': 'UJlA6_Ij4Pw',
            'text': FAKE.paragraph(),
            },
        ]

        for idx, fake in enumerate(fakes):
            self.create_explainer(fake, idx)

    def create_explainer(self, data, order):
        explainer, _ = Explainer.objects.get_or_create(
            title=data['title'],
            youtube_id=data['youtube_id'],
            text=data['text'],
            order=order,
        )
