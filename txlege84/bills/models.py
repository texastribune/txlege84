from django.db import models

from committees.models import Committee
from legislators.models import Chamber, Legislator


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Bill(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField()
    chamber = models.ForeignKey(Chamber, related_name='bills')
    sponsors = models.ManyToManyField(Legislator, through='Sponsorship')
    subjects = models.ManyToManyField(Subject, related_name='bills')
    openstates_id = models.CharField(max_length=11, unique=True)
    bill_type = models.CharField(max_length=21)

    # consider these a bit longer
    # first_action_date = models.DateField(null=True, blank=True)
    # last_action_date = models.DateField(null=True, blank=True)
    # passed_senate = models.DateField(null=True, blank=True)
    # passed_house = models.DateField(null=True, blank=True)
    # became_law = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Action(models.Model):
    number = models.CharField(max_length=4)
    text = models.CharField(max_length=100)
    date = models.DateField()
    acting_chamber = models.ForeignKey(Chamber, related_name='actions')
    related_committee = models.ForeignKey(
        Committee, related_name='actions', null=True, blank=True)
    bill = models.ForeignKey(Bill, related_name='actions')


class Sponsorship(models.Model):
    legislator = models.ForeignKey(Legislator, related_name='sponsorships')
    bill = models.ForeignKey(Bill, related_name='sponsorships')
    role = models.CharField(max_length=20)

    def __unicode__(self):
        return u'{0} as {1} of {2}'.format(
            self.legislator.full_name, self.role, self.bill)
