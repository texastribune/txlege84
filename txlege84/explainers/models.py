from django.db import models
from django.utils.text import slugify


class Explainer(models.Model):
    name = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=11)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField()

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:50]
