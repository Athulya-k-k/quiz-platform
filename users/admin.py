# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for custom User model
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_admin',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('is_admin',)}),
    )
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_admin', 'is_staff', 'is_active', 'date_joined')