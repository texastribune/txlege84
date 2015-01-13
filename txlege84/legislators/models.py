from django.db import models
from django.utils.text import slugify


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


class Legislator(models.Model):
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
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

    capitol_address = models.TextField(null=True, blank=True)
    capitol_phone = models.CharField(max_length=12, null=True, blank=True)

    district_address = models.TextField(null=True, blank=True)
    district_phone = models.CharField(max_length=12, null=True, blank=True)

    openstates_id = models.CharField(max_length=9, unique=True)

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
