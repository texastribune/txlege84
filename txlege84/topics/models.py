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
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Topic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('topic-detail', args=(self.slug,))


class IssueText(models.Model):
    issue = models.ForeignKey('Issue', related_name='texts')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_date',)


class Issue(models.Model):
    name = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='issues')
    slug = models.SlugField()
    image = models.URLField(null=True, blank=True)
    active_text = models.ForeignKey(IssueText, related_name='issues')
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=1, choices=PUBLICATION_CHOICES, default=u'D')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    related_bills = models.ManyToManyField(
        Bill, related_name='issues', null=True, blank=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Issue, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('issue-detail', args=(self.topic.slug, self.slug,))

    def get_admin_url(self):
        from django.core.urlresolvers import reverse
        return reverse('admin:{0}_{1}_change'.format(
            self._meta.app_label, self._meta.module_name), args=(self.id,))


class StoryPointer(models.Model):
    headline = models.CharField(max_length=200)
    url = models.URLField()
    pub_date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    issue = models.ForeignKey(Issue, related_name='stories')

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.headline


class TopIssue(models.Model):
    issue = models.ForeignKey(Issue, related_name='top_issue')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return u'{0} (Top Issue #{1})'.format(self.issue.name, self.order)
