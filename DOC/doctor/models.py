from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User

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

class Doctor(models.Model):
    name = models.CharField(max_length=100, null = True, blank = True)
    designation = models.CharField(max_length=500, null = True, blank = True)
    qualification = models.CharField(max_length=500, null = True, blank = True)
    experience = models.CharField(max_length=100, null = True, blank = True)
    specialists = models.ManyToManyField(Specialist, blank = True,)
    license_no = models.CharField(max_length=100, null = True, blank = True)
    slug = models.CharField(max_length=100, null = True, blank = True)

    def __str__(self):
        return self.name
    
class Chamber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='chamber', null = True, blank = True)
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