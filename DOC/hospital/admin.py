from django.contrib import admin
from .models import Hospital
# Register your models here.
class HospitalModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ('name',)}
    list_display = (
        'id',
        'name',
        'address',
        'availability',
        'phone_number',
        'category',
    )
    list_filter = (
        'specialists__specialist_name',
        'services__service_name',
    )
    search_fields = (
        'name','address'
    )

admin.site.register(Hospital,HospitalModelAdmin)