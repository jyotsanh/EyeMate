from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    def has_add_permission(self, request):
        """
        Override the default behavior to prevent users from creating new users
        through the admin interface.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Override the default behavior to prevent users from deleting users
        through the admin interface.
        """
        return False

    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read-only in the admin interface.
        """
        return self.get_fields(request, obj)

    list_display = ('id', 'username', 'is_admin', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('id',)
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)
