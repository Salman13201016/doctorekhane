from django.contrib import admin
from .models import Doctor, Chamber, Experience, DoctorService, Review
# Register your models here.
class DoctorModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ('name',)}
    list_display = (
        'id',
        'user',
        'name',
        'experience_year',
        'license_no',
    )
    list_filter = (
        'qualification',
        'specialists__specialist_name',
    )
    search_fields = (
        'name','specialists__specialist_name'
    )

class ChamberModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'doctor',
        'fee',
        'availability',
    )

class ExperienceModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'doctor',
        'start_date',
        'end_date',
        'working_place',
        'designation',
    )
    list_filter = (
        'start_date',
        'end_date',
        'doctor',
    )
    search_fields = (
        'working_place',
    )

class ReviewModelAdmin(admin.ModelAdmin):
    list_display=(
        'id',
        'doctor',
        'rating',
        'created_at',
    )
    search_fields = (
        'doctor__name',
        'rating',
    )


admin.site.register(DoctorService,list_display=('id','doctor','service_name'))
admin.site.register(Doctor,DoctorModelAdmin)
admin.site.register(Chamber,ChamberModelAdmin)
admin.site.register(Experience,ExperienceModelAdmin)
admin.site.register(Review, ReviewModelAdmin)