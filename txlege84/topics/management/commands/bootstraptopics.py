from django.core.management.base import BaseCommand

from topics.models import Topic


class Command(BaseCommand):
    help = u'Bootstrap the topic lists in the database.'

    def handle(self, *args, **kwargs):
        self.load_topics()

    def load_topics(self):
        self.stdout.write(u'Loading hot list topics...')

        topics = [
            u'Budget & Taxes',
            u'Criminal Justice',
            u'Energy',
            u'Environment',
            u'Ethics',
            u'Health & Human Services',
            u'Higher Education',
            u'Immigration & Border Security',
            u'Public Education',
            u'Social Justice',
            u'Transportation',
        ]

        for topic in topics:
            Topic.objects.get_or_create(name=topic)
