from django.contrib import admin

from bills.models import Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    pass
