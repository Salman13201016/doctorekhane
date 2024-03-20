from django.contrib import admin
from .models import DoctorAppointment
# Register your models here.
class DoctorAppointmentAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "appointment_id",
        "user",
        "doctor",
        "chamber",
        )
    list_filter = (
        'patientstatus',
        'doctor',
        'user',
    )
    search_fields = (
        'doctor','appointment_id','user'
    )
    
admin.site.register(DoctorAppointment,DoctorAppointmentAdmin)

