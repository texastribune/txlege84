
from faker import Factory

from django.core.management.base import BaseCommand

from bills.models import Bill
from topics.models import (Issue, IssueText,
                           StoryPointer, Topic, TopIssue)

FAKE = Factory.create()


class Command(BaseCommand):
    help = u'Load fake issues into the database. For development ONLY.'

    def handle(self, *args, **kwargs):
        self.load_fake_issues()

    def load_fake_issues(self):
        self.stdout.write(u'Loading fake issues...')

        issue_loader = {
            "Immigration & Border Security": [
                "Banning \"sanctuary cities\"",
                "Border security spending and operations",
                "Mandating the use of E-Verify"
            ],
            "Budget & Taxes": [
                "Providing property tax relief",
                "Reducing the margins tax burden",
                "Budget fallout from school finance lawsuit"
            ],
            "Law & Order": [
                "Enhancing gun rights",
                "Efforts to change Voter ID",
                "Reducing penalties for marijuana possession",
                "Changing the age of adulthood for criminal charges"
            ],
            "Energy": [
                "Acting on the EPA's \"Clean Power Plan\"",
                "Responding to volatile oil prices",
                "Combatting local drilling ordinances"
            ],
            "Environment": [
                "Reforming how groundwater is managed",
                "Chipping away at environmental regulations",
                "Addressing the effects of oil and gas drilling"
            ],
            "Ethics": [
                "The fight over \"dark money\"",
                "Former legislators as lobbyists"
            ],
            "Health & Human Services": [
                "Consolidating Texas' health agencies",
                "Medicaid expansion or its alternatives",
                "Reforming end-of-life care"
            ],
            "Higher Education": [
                "Tuition revenue bonds for campus construction",
                "In-state tuition for undocumented students",
                "Reining in rising tuition"
            ],
            "Public Education": [
                "Improving educator quality",
                "Reforming pre-K",
                "School choice and vouchers"
            ],
            "Transportation": [
                "Ensuring all gas tax revenue goes to the highway fund",
                "Dedicating car sales taxes to the highway fund",
                "Reviewing state policies on toll roads"
            ],
            "Social Issues": [
                "Efforts to advance equal rights legislation",
                "Further restrictions on abortion",
                "Expanding gambling in Texas"]
            }

        for topic in Topic.objects.all():
            for issue in issue_loader[topic.name]:
                self.create_issue(topic, issue)

        self.create_top_issues()

    def create_issue(self, topic, issue):
        issue_name = unicode(issue)
        issue_text = FAKE.paragraphs(nb=FAKE.random_int(2, 4))
        issue_text = ''.join(['<p>{}</p>'.format(p) for p in issue_text])

        num_of_issues = topic.issues.count()

        issue_text, _ = IssueText.objects.get_or_create(
            text=issue_text,
        )

        issue, _ = Issue.objects.get_or_create(
            name=issue_name,
            topic=topic,
            order=num_of_issues + 1,
            status='P',
            active_text=issue_text
        )

        issue_text.issue = issue
        issue_text.save()

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
        for n in xrange(FAKE.random_int(0, 10)):
            pointer, _ = StoryPointer.objects.get_or_create(
                headline=FAKE.sentence(nb_words=8)[:-1],
                issue=issue,
                url=FAKE.uri(),
                order=n,
                pub_date=FAKE.date(),
            )

    def create_top_issues(self):
        random_issues = Issue.objects.order_by('?')[:4]

        for idx, issue in enumerate(random_issues):
            topIssue, _ = TopIssue.objects.get_or_create(
                issue=issue,
                order=idx + 1)
