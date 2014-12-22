from django.conf import settings
from django.db import models
from django.utils.text import slugify

from bills.models import Bill


PUBLICATION_CHOICES = (
    (u'D', u'Draft'),
    (u'P', u'Published'),
    (u'W', u'Withdrawn'),
)


class Topic(models.Model):
    name = models.CharField(max_length=20, unique=True)
    curators = models.ManyToManyField(settings.AUTH_USER_MODEL)
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Topic, self).save(*args, **kwargs)


class Issue(models.Model):
    name = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='issues')
    active_text = models.OneToOneField('IssueText', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    order = models.IntegerField()
    status = models.CharField(
        max_length=1, choices=PUBLICATION_CHOICES, default=u'D')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    related_bills = models.ManyToManyField(Bill, related_name='issues')

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Issue, self).save(*args, **kwargs)


class IssueText(models.Model):
    associated_issue = models.ForeignKey(Issue, related_name='texts')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Stream(models.Model):
    issue = models.OneToOneField(Issue, related_name='stream_of')


class StoryPointer(models.Model):
    headline = models.CharField(max_length=200)
    url = models.URLField()

    order = models.IntegerField()
    active = models.BooleanField(default=False)

    stream = models.ForeignKey(Stream, related_name='stories')
