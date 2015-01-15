from django.contrib.auth.models import User
from django.db import models

from legislators.models import Chamber


class Staff(models.Model):
    user = models.OneToOneField(User)
    profile_photo = models.URLField()


class ConveneTime(models.Model):
    chamber = models.OneToOneField(Chamber, related_name='time_for')
    time_string = models.CharField(max_length=100)

    def __unicode__(self):
        return u'Time for {}'.format(self.chamber)
