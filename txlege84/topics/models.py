from django.db import models
from django.utils.text import slugify

from bills.models import Bill


class Topic(models.Model):
    name = models.CharField(max_length=20, unique=True)
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
    text = models.TextField()
    slug = models.SlugField(null=True, blank=True)
    photo = models.URLField(null=True, blank=True)

    order = models.IntegerField()
    active = models.BooleanField(default=False)

    related_bills = models.ManyToManyField(Bill, related_name='issues')

    class Meta:
        ordering = ('order',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Issue, self).save(*args, **kwargs)


class Stream(models.Model):
    issue = models.OneToOneField(Issue, related_name='stream_of')


class StoryPointer(models.Model):
    headline = models.CharField(max_length=200)
    url = models.URLField()

    order = models.IntegerField()
    active = models.BooleanField(default=False)

    stream = models.ForeignKey(Stream, related_name='stories')
