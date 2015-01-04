from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.safestring import mark_safe

from adminsortable.admin import SortableAdminMixin, SortableInlineAdminMixin

from topics.models import (
    Issue, IssueText, StoryPointer, Stream, Topic, TopIssue)


class IssueTextAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={
                'class': 'ckeditor',
            })
        }
    }

    class Media:
        js = ('ckeditor/ckeditor.js', )


class IssueTextInline(admin.TabularInline):
    model = IssueText

    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={
                'class': 'ckeditor',
            })
        }
    }

    class Media:
        js = ('ckeditor/ckeditor.js', )

    extra = 0


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})}
    }

    fieldsets = (
        ('Meta', {
            'fields': ('name', 'slug', 'topic', 'status',)
        }),
        ('Bills', {
            'fields': ('related_bills',)
        }),
        ('Story Stream', {
            'fields': ('story_stream',)
        })
    )

    filter_horizontal = ('related_bills',)

    inlines = (IssueTextInline,)

    list_display = ('name', 'topic', 'status', 'modified_date',)

    list_filter = ('topic', 'status',)

    prepopulated_fields = {'slug': ('name',)}

    radio_fields = {
        'status': admin.HORIZONTAL,
    }

    readonly_fields = ('story_stream',)

    save_on_top = True

    search_fields = ('name',)

    def story_stream(self, model):
        return mark_safe(
            '<a href="{}" target="_blank">Edit story stream</a>'.format(
                model.stream_of.get_admin_url()))


class IssueInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Issue

    extra = 0

    fields = ('name', 'order', 'view', 'edit',)

    readonly_fields = ('name', 'view', 'edit',)

    max_num = 0

    def view(self, model):
        return mark_safe(
            '<a href="{}" target="_blank">View on site</a>'.format(
                model.get_absolute_url()))

    def edit(self, model):
        return mark_safe(
            '<a href="{}">Edit this issue</a>'.format(model.get_admin_url()))


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})}
    }

    fieldsets = (
        ('Meta', {
            'fields': ('name', 'slug',)
        }),
        ('Curators', {
            'classes': ('collapse',),
            'fields': ('curators',)
        })
    )

    filter_horizontal = ('curators',)

    inlines = (IssueInline,)

    prepopulated_fields = {'slug': ('name',)}

    save_on_top = True


@admin.register(TopIssue)
class TopIssueAdmin(SortableAdminMixin, admin.ModelAdmin):
    fields = ('issue',)

    raw_id_fields = ('issue',)


class StoryPointerInline(SortableInlineAdminMixin, admin.TabularInline):
    model = StoryPointer

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})}
    }

    fields = ('headline', 'url', 'order',)

    extra = 0


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    inlines = (StoryPointerInline,)

    readonly_fields = ('issue',)
