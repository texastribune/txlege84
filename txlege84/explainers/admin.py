from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput

from explainers.models import Explainer

from adminsortable.admin import SortableAdminMixin


@admin.register(Explainer)
class ExplainerAdmin(SortableAdminMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={
                'size': '80'
            })
        },
        models.TextField: {
            'widget': forms.Textarea(attrs={
                'class': 'ckeditor',
            })
        }
    }

    fields = ('name', 'slug', 'status', 'youtube_id', 'text',)

    list_display = ('name', 'youtube_id', 'created_date', 'modified_date',)

    save_on_top = True

    prepopulated_fields = {'slug': ('name',)}

    radio_fields = {
        'status': admin.HORIZONTAL,
    }

    class Media:
        js = ('ckeditor/ckeditor.js',)
