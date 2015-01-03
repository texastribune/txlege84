from django.contrib import admin

from topics.models import Issue, StoryPointer, Stream, Topic


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Topic)
admin.site.register(Stream)
admin.site.register(StoryPointer)
