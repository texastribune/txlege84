
from faker import Factory

from django.core.management.base import BaseCommand

from bills.models import Bill
from topics.models import (Issue, IssueText,
                           StoryPointer, Stream, Topic, TopIssue)

FAKE = Factory.create()


class Command(BaseCommand):
    help = u'Load fake issues into the database. For development ONLY.'

    def handle(self, *args, **kwargs):
        self.load_fake_issues()

    def load_fake_issues(self):
        self.stdout.write(u'Loading fake issues...')

        for topic in Topic.objects.all():
            for _ in xrange(FAKE.random_int(1, 10)):
                self.create_issue(topic)

        self.create_top_issues()

    def create_issue(self, topic):
        issue_name = FAKE.sentence(nb_words=8)[:-1]  # no period
        issue_text = FAKE.paragraphs(nb=FAKE.random_int(2, 4))
        issue_text = ''.join(['<p>{}</p>'.format(p) for p in issue_text])

        num_of_issues = topic.issues.count()

        issue, _ = Issue.objects.get_or_create(
            name=issue_name,
            topic=topic,
            order=num_of_issues + 1,
            status='P',
        )

        issue_text, _ = IssueText.objects.get_or_create(
            associated_issue=issue,
            text=issue_text,
        )

        issue.active_text = issue_text
        issue.save()

        for _ in xrange(FAKE.random_int(0, 3)):
            random_bill = Bill.objects.filter(
                bill_type='bill',
                chamber__name='Texas House').order_by('?')[0]

            issue.related_bills.add(random_bill)

        for _ in xrange(FAKE.random_int(0, 3)):
            random_bill = Bill.objects.filter(
                bill_type='bill',
                chamber__name='Texas Senate').order_by('?')[0]

            issue.related_bills.add(random_bill)

        self.create_stream(issue)

    def create_stream(self, issue):
        stream, _ = Stream.objects.get_or_create(
            issue=issue)

        for n in xrange(FAKE.random_int(0, 10)):
            pointer, _ = StoryPointer.objects.get_or_create(
                headline=FAKE.sentence(nb_words=8)[:-1],
                stream=stream,
                url=FAKE.uri(),
                order=n,
            )

    def create_top_issues(self):
        random_issues = Issue.objects.order_by('?')[:4]

        for idx, issue in enumerate(random_issues):
            topIssue, _ = TopIssue.objects.get_or_create(
                issue=issue,
                order=idx + 1)
