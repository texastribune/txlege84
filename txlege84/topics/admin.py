from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.safestring import mark_safe

from adminsortable.admin import SortableInlineAdminMixin

from topics.models import (
    FeaturedTopic, Issue, IssueText, StoryPointer, Topic)


@admin.register(IssueText)
class IssueTextAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={
                'class': 'ckeditor',
            })
        }
    }

    list_display = ('issue', 'created_date', 'modified_date',)

    class Media:
        js = ('ckeditor/ckeditor.js',)


class StoryPointerInline(admin.TabularInline):
    model = StoryPointer

    exclude = ('order',)

    extra = 1


class IssueTextInline(admin.TabularInline):
    model = IssueText

    fields = ('text', 'issue',)

    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={
                'class': 'ckeditor',
            })
        }
    }

    readonly_fields = ('issue',)

    class Media:
        js = ('ckeditor/ckeditor.js',)

    extra = 0


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})}
    }

    fieldsets = (
        ('Meta', {
            'fields': ('name', 'slug', 'topic', 'status', 'active_text',)
        }),
        ('Bills', {
            'fields': ('related_bills',)
        }),
    )

    raw_id_fields = ('active_text',)

    filter_horizontal = ('related_bills',)

    inlines = (StoryPointerInline,)

    list_display = ('name', 'topic', 'status', 'modified_date',)

    list_filter = ('topic', 'status',)

    prepopulated_fields = {'slug': ('name',)}

    radio_fields = {
        'status': admin.HORIZONTAL,
    }

    save_on_top = True

    search_fields = ('name',)


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
            'fields': ('curators',)
        })
    )

    filter_horizontal = ('curators',)

    inlines = (IssueInline,)

    prepopulated_fields = {'slug': ('name',)}

    save_on_top = True


@admin.register(FeaturedTopic)
class FeaturedTopicAdmin(admin.ModelAdmin):
    fields = ('topic',)

    raw_id_fields = ('topic',)


class StoryPointerInline(SortableInlineAdminMixin, admin.TabularInline):
    model = StoryPointer

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})}
    }

    fields = ('headline', 'url', 'order',)

    extra = 0
