from django.contrib import admin
from .models import Goal,OthersContent,SiteSettings,Notice,Divisions,Districts,Upazilas,Services,Specialist,Team,ActionLog,Notifications,FAQ
# Register your models here.
admin.site.register(Divisions,list_display=('id','division_name',))
admin.site.register(Districts,list_display=('id','district_name',))
admin.site.register(Upazilas,list_display=('id','upazila_name'))
admin.site.register(Specialist,list_display=('id','specialist_name'))
admin.site.register(Services,list_display=('id','service_name'))
admin.site.register(Team)
admin.site.register(ActionLog)
admin.site.register(Notifications)
admin.site.register(Notice)
admin.site.register(SiteSettings)
admin.site.register(Goal)
admin.site.register(OthersContent)
admin.site.register(FAQ)

