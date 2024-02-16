from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from app.models import ROLES, Unions
from django.utils.text import slugify

# Create your models here.
RATING_TYPE_CHOICES=[
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
]

class Specialist(models.Model):
    specialist_name = models.CharField(max_length=100,blank=True,null=True)
    specialist_logo = ResizedImageField(upload_to = 'specialist_logo/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.img.storage, self.img.path
        # Delete the model before the file
        super(Specialist, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
            
class Doctor(models.Model):
    name = models.CharField(max_length=100, null = True, blank = True)
    designation = models.CharField(max_length=500, null = True, blank = True)
    qualification = models.CharField(max_length=500, null = True, blank = True)
    profile_image = ResizedImageField(upload_to='Doctor_Profile/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    experience_year = models.CharField(max_length=100, null = True, blank = True)
    specialists = models.ManyToManyField(Specialist, blank = True,)
    license_no = models.CharField(max_length=100, null = True, blank = True)
    slug = models.CharField(max_length=100, null = True, blank = True)
    role = models.CharField(max_length=50, null=False, default="doctor", choices=ROLES)
    location = models.ForeignKey(Unions, on_delete=models.CASCADE, blank = True , null = True)
    address = models.TextField(max_length=500, blank=True, null=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Doctor, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.img.storage, self.img.path
        # Delete the model before the file
        super(Doctor, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
    
class Chamber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='chamber', null = True, blank = True)
    hospital = models.CharField(max_length=500, null = True, blank = True)
    address = models.CharField(max_length=500, null = True, blank = True)
    fee = models.CharField(max_length=500, null = True, blank = True)
    availability = models.CharField(max_length=500, null = True, blank = True)

    def __str__(self):
        return self.doctor.name

class Experience(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='experiences', null = True, blank = True)
    start_date = models.DateField(null = True, blank = True)
    end_date = models.DateField(null = True, blank = True)
    designation = models.CharField(max_length=500, null = True, blank = True)
    working_place = models.CharField(max_length=500, null = True, blank = True)

    def __str__(self):
        return self.doctor.name
    
class DoctorService(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='services', null = True, blank = True)
    service_name = models.CharField(max_length=500, null = True, blank = True)

    def __str__(self):
        return self.doctor.name

class Review(models.Model):
    user = models.ForeignKey(User, null=True,on_delete=models.SET_NULL,blank=True)
    # order = models.ForeignKey("sale.Order", on_delete=models.CASCADE,null=True,blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='review',null=True,blank=True)
    rating=models.IntegerField(choices=RATING_TYPE_CHOICES,blank=True,null=True)
    content = models.TextField(max_length=1500,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'doctor')