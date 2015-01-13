from django.contrib import admin

from legislators.models import Legislator


@admin.register(Legislator)
class LegislatorAdmin(admin.ModelAdmin):
    pass
