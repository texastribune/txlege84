from django.db import models
from django.utils.text import slugify

from txlege84.managers import PublishedQuerySet

PUBLICATION_CHOICES = (
    (u'D', u'Draft'),
    (u'P', u'Published'),
    (u'W', u'Withdrawn'),
)


class Explainer(models.Model):
    name = models.CharField(u'title', max_length=200)
    youtube_id = models.CharField(u'YouTube ID', max_length=11)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField()
    status = models.CharField(
        max_length=1, choices=PUBLICATION_CHOICES, default=u'D')

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:50]

        super(Explainer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('explainer-detail', args=(self.slug,))
