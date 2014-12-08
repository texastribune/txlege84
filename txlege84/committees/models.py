from django.db import models
from django.utils.text import slugify

from legislators.models import Chamber, Legislator


class Committee(models.Model):
    name = models.CharField(max_length=60)
    chamber = models.ForeignKey(Chamber, related_name='committees')
    openstates_id = models.CharField(max_length=9, unique=True)
    members = models.ManyToManyField(Legislator, through='Membership')
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Committee, self).save(*args, **kwargs)


class Membership(models.Model):
    legislator = models.ForeignKey(Legislator, related_name='memberships')
    committee = models.ForeignKey(Committee, related_name='memberships')
    role = models.CharField(max_length=20)

    def __unicode__(self):
        return '{0} in {1}'.format(self.role, self.committee.name)


class Event(models.Model):
    pass
