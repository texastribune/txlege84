from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from legislators.models import Chamber


class Staff(models.Model):
    user = models.OneToOneField(User)
    profile_photo = models.URLField()


class ConveneTime(models.Model):
    chamber = models.OneToOneField(Chamber, related_name='time_for')
    time_string = models.CharField(max_length=100)
    status = models.CharField(max_length=40, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Time for {}'.format(self.chamber)

    @property
    def stream_is_live(self):
        if (self.time < timezone.now()) and self.active:
            return True
        return False
