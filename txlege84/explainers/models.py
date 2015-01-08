from django.db import models


class Explainer(models.Model):
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=11)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.title
