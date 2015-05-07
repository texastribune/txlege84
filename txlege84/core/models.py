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


class Stream(models.Model):
    chamber = models.OneToOneField(
        Chamber,
        help_text='Chamber viewable in stream',
        related_name='stream_for')
    granicus_subdomain = models.CharField(
        help_text='Granicus subdomain for stream', max_length=20)
    camera_id = models.IntegerField(
        help_text='Identifier for direct camera stream')
    direct_event_feed = models.BooleanField(
        help_text='Use an event feed instead of a camera feed',
        default=False)
    feed_id = models.IntegerField(
        help_text='Feed identifier for direct embed',
        null=True, blank=True)
    event_id = models.IntegerField(
        help_text='Event identifier for direct embed',
        null=True, blank=True)

    def __unicode__(self):
        return u'Stream for {}'.format(self.chamber)
