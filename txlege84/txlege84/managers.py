from django.db import models


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=u'P')


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)
