from django.contrib import admin
from .models import Divisions,Districts,Upazilas,Unions,Services,Specialist
# Register your models here.
admin.site.register(Divisions,list_display=('id','division_name',))
admin.site.register(Districts,list_display=('id','district_name',))
admin.site.register(Upazilas,list_display=('id','upazila_name'))
admin.site.register(Unions,list_display=('id','union_name'))
admin.site.register(Specialist,list_display=('id','specialist_name'))
admin.site.register(Services,list_display=('id','service_name'))
