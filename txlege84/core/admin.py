from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import Staff


class EmployeeInline(admin.StackedInline):
    model = Staff
    can_delete = False
    verbose_name_plural = 'members'


class UserAdmin(UserAdmin):
    inlines = (EmployeeInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
