from django.db import models
from django.db.models import Q
from django.utils.text import slugify

from txlege84.managers import ActiveQuerySet


class Party(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    @property
    def short_name(self):
        if self.name == 'Republican':
            return u'R'
        elif self.name == 'Democratic':
            return u'D'
        else:
            return u''


class Chamber(models.Model):
    name = models.CharField(max_length=12)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:50]

        super(Chamber, self).save(*args, **kwargs)

    @property
    def member_title(self):
        if self.name == 'Texas House':
            return u'Representative'
        elif self.name == 'Texas Senate':
            return u'Senator'
        else:
            return u''

    @property
    def short_name(self):
        if self.name == 'Texas House':
            return u'Rep.'
        elif self.name == 'Texas Senate':
            return u'Sen.'

    @property
    def chamber_name(self):
        if self.name == 'Texas House':
            return u'House'
        if self.name == 'Texas Senate':
            return u'Senate'


class Legislator(models.Model):
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40)
    party = models.ForeignKey(
        Party, related_name='legislators', null=True, blank=True)
    chamber = models.ForeignKey(
        Chamber, related_name='legislators', null=True, blank=True)
    district = models.IntegerField(null=True, blank=True)
    profile_url = models.URLField(null=True, blank=True)
    active = models.BooleanField(default=False)
    slug = models.SlugField()

    tribune_slug = models.SlugField(null=True, blank=True)
    tribune_photo = models.URLField(null=True, blank=True)
    tribune_city = models.CharField(max_length=40, null=True, blank=True)
    tribune_room = models.CharField(max_length=20, null=True, blank=True)

    capitol_address = models.TextField(null=True, blank=True)
    capitol_phone = models.CharField(max_length=12, null=True, blank=True)

    district_address = models.TextField(null=True, blank=True)
    district_phone = models.CharField(max_length=12, null=True, blank=True)

    openstates_id = models.CharField(max_length=9, unique=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        ordering = ('last_name',)

    def __unicode__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.full_name)[:50]

        super(Legislator, self).save(*args, **kwargs)

    @property
    def full_name(self):
        if self.middle_name:
            return u'{0} {1} {2}'.format(
                self.first_name, self.middle_name, self.last_name)

        return u'{0} {1}'.format(self.first_name, self.last_name)

    @property
    def last_first_full_name(self):
        if self.middle_name:
            return u'{0}, {1} {2}'.format(
                self.last_name, self.first_name, self.middle_name)

        return u'{0}, {1}'.format(self.last_name, self.first_name)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('legislator-detail', args=(self.slug,))

    @property
    def tribune_directory_url(self):
        return u'https://www.texastribune.org/directory/{}/'.format(
            self.tribune_slug)

    @property
    def tribune_ethics_url(self):
        return u'https://www.texastribune.org/bidness/explore/{}/'.format(
            self.tribune_slug)

    @property
    def chair_memberships(self):
        return self.memberships.filter(role='Chair')

    @property
    def vicechair_memberships(self):
        return self.memberships.filter(role='Vice Chair')

    @property
    def member_memberships(self):
        return self.memberships.filter(role='Member')

    @property
    def authored_bills(self):
        return self.sponsorships.filter(role='author')

    @property
    def new_laws(self):
        return self.authored_bills.filter(
            bill__became_law__isnull=False).select_related('bill')

    @property
    def vetoed_bills(self):
        return self.authored_bills.filter(
            bill__vetoed__isnull=False).select_related('bill')

    @property
    def passed_house_and_senate(self):
        return self.authored_bills.filter(
            bill__passed_house__isnull=False,
            bill__passed_senate__isnull=False).select_related('bill')

    @property
    def failed_bills(self):
        return self.authored_bills.filter(
            Q(bill__passed_house__isnull=True) |
            Q(bill__passed_senate__isnull=True)).select_related('bill')
