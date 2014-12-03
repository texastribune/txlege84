from django.contrib import admin

from topics.models import Issue, StoryPointer, Stream, Topic

admin.site.register(Topic)
admin.site.register(Issue)
admin.site.register(Stream)
admin.site.register(StoryPointer)
