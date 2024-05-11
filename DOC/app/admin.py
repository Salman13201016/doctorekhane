from django.contrib import admin
from .models import Notice,Divisions,Districts,Upazilas,Unions,Services,Specialist,Team,ActionLog,Notifications
# Register your models here.
admin.site.register(Divisions,list_display=('id','division_name',))
admin.site.register(Districts,list_display=('id','district_name',))
admin.site.register(Upazilas,list_display=('id','upazila_name'))
admin.site.register(Unions,list_display=('id','union_name'))
admin.site.register(Specialist,list_display=('id','specialist_name'))
admin.site.register(Services,list_display=('id','service_name'))
admin.site.register(Team)
admin.site.register(ActionLog)
admin.site.register(Notifications)
admin.site.register(Notice)
