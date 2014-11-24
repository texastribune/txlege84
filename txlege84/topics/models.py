from django.db import models

from bills.models import Bill


class Topic(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Issue(models.Model):
    name = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='issues')
    text = models.TextField()

    order = models.IntegerField()
    active = models.BooleanField(default=False)

    related_bills = models.ManyToManyField(Bill, related_name='issues')

    class Meta:
        ordering = ('order',)


class Stream(models.Model):
    issue = models.OneToOneField(Issue, related_name='stream_of')


class StoryPointer(models.Model):
    headline = models.CharField(max_length=200)
    url = models.URLField()

    order = models.IntegerField()
    active = models.BooleanField(default=False)

    stream = models.ForeignKey(Stream, related_name='stories')
