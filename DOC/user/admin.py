from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from user.models import Profile

# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role'),
        }),
    )

class ProfileModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone_number',
        'address',
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileModelAdmin)
