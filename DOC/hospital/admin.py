from django.contrib import admin
from .models import Hospital,Ambulance,Test,TestCatagory
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

class AmbulanceModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ('name',)}
    list_display = (
        'id',
        'name',
        'ac',
        'hospital',
        'phone_number',
    )
    list_filter = (
        'ac',
        'hospital',
    )
    search_fields = (
        'name','address'
    )

class TestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ('test_name',)}
    list_display = (
        'id',
        'catagory',
        'test_name',
        'fee',
        'delivery_time',
    )
    list_filter = (
        'catagory',
    )
    search_fields = (
        'test_name',
    )

admin.site.register(TestCatagory)
admin.site.register(Test,TestAdmin)
admin.site.register(Hospital,HospitalModelAdmin)
admin.site.register(Ambulance,AmbulanceModelAdmin)