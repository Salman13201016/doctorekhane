from django.contrib import admin

from user.models import Profile

# Register your models here.
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'role',
        'phone_number',
        'address',
    )

admin.site.register(Profile, ProfileModelAdmin)