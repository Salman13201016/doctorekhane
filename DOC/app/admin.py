from django.contrib import admin
from .models import Division,District,State
# Register your models here.
admin.site.register(Division,list_display=('id','name',))
admin.site.register(District,list_display=('id','name',))
admin.site.register(State,list_display=('id','name',))
