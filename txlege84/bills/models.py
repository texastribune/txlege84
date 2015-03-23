from django.db import models
from django.utils.text import slugify

from committees.models import Committee
from legislators.models import Chamber, Legislator


BILL_TYPES = {
    'HB': 'House Bill',
    'SB': 'Senate Bill',
    'HR': 'House Resolution',
    'SR': 'Senate Resolution',
    'HJR': 'House Joint Resolution',
    'SJR': 'Senate Joint Resolution',
    'HCR': 'House Concurrent Resolution',
    'SCR': 'Senate Concurrent Resolution',
}


class Subject(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:50]

        super(Subject, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('category-detail', args=(self.slug,))


class Bill(models.Model):
    name = models.CharField(max_length=10)
    bill_number = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    chamber = models.ForeignKey(Chamber, related_name='bills')
    sponsors = models.ManyToManyField(Legislator, through='Sponsorship')
    subjects = models.ManyToManyField(Subject, related_name='bills')
    openstates_id = models.CharField(max_length=11, unique=True)
    bill_type = models.CharField(max_length=21)
    slug = models.SlugField()

    first_action_date = models.DateField(null=True, blank=True)
    last_action_date = models.DateField(null=True, blank=True)
    passed_senate = models.DateField(null=True, blank=True)
    passed_house = models.DateField(null=True, blank=True)
    became_law = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('chamber__name', 'bill_type', 'bill_number',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = self.name.replace(' ', '')

        super(Bill, self).save(*args, **kwargs)

    @property
    def house_committee(self):
        try:
            return self.actions.reverse().exclude(
                related_committee__isnull=True).filter(
                acting_chamber__name='Texas House')[0].related_committee
        except IndexError:
            return None

    @property
    def senate_committee(self):
        try:
            return self.actions.reverse().exclude(
                related_committee__isnull=True).filter(
                acting_chamber__name='Texas Senate')[0].related_committee
        except IndexError:
            return None

    @property
    def long_name(self):
        split_name = self.name.split(' ')

        return '{0} {1}'.format(
            BILL_TYPES[split_name[0]], split_name[1])

    @property
    def authors(self):
        return self.sponsorships.filter(role='author')

    @property
    def coauthors(self):
        return self.sponsorships.filter(role='coauthor')

    @property
    def sponsors(self):
        return self.sponsorships.filter(role='sponsor')

    @property
    def cosponsors(self):
        return self.sponsorships.filter(role='cosponsor')

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('bill-detail', args=(self.slug,))


class Action(models.Model):
    number = models.CharField(max_length=4)
    text = models.CharField(max_length=100)
    date = models.DateField()
    acting_chamber = models.ForeignKey(Chamber, related_name='actions')
    related_committee = models.ForeignKey(
        Committee, related_name='actions', null=True, blank=True)
    bill = models.ForeignKey(Bill, related_name='actions')

    class Meta:
        ordering = ['date', 'pk']


class Sponsorship(models.Model):
    legislator = models.ForeignKey(Legislator, related_name='sponsorships')
    bill = models.ForeignKey(Bill, related_name='sponsorships')
    role = models.CharField(max_length=20)

    def __unicode__(self):
        return u'{0} as {1} of {2}'.format(
            self.legislator.full_name, self.role, self.bill)
