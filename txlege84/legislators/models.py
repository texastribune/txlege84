from django.db import models


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

    def __unicode__(self):
        return self.name


class Legislator(models.Model):
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    party = models.ForeignKey(Party, related_name='legislators')
    chamber = models.ForeignKey(
        Chamber, related_name='legislators', null=True, blank=True)
    district = models.IntegerField(null=True, blank=True)
    profile_url = models.URLField()

    openstates_id = models.CharField(max_length=9, unique=True)

    def __unicode__(self):
        return self.full_name

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
