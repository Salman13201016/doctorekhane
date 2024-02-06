from django.db import models
from app.models import District, Division, State
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField


class Hospital(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)
    division = models.ForeignKey(Division,on_delete=models.CASCADE,blank=True,null=True )  
    district = models.ForeignKey(District,on_delete=models.CASCADE,blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,blank=True,null=True)
    postal_code = models.IntegerField(null=True,blank=True) 
    address = models.TextField(max_length=500, blank=True, null=False)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    longitude = models.CharField(max_length=100,null=True, blank=True)
    latitude = models.CharField(max_length=100,null=True, blank=True)
    slug = models.SlugField(unique=True)


    # Hospital Profile Fields
    hospital_image = ResizedImageField(upload_to='hospital/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    facilities = RichTextField(blank=True, null=True)
    services_offered = models.TextField(null=True, blank=True)
    specialties = models.TextField(null=True, blank=True)
    accreditation_details = RichTextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)
    is_emergency_services_available = models.BooleanField(default=False)
    is_pharmacy_available = models.BooleanField(default=False)
    is_ambulance_available = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)

  
    def __str__(self):
        return self.name
    

