from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    UserAdmin.list_display += ('role', 'bio', 'is_active')
    UserAdmin.fieldsets[1][1]['fields'] += ('bio',)
    UserAdmin.fieldsets[2][1]['fields'] += ('role',)
