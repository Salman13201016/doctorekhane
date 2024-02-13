from django.db import models
from app.models import Unions
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from app.models import ROLES


GENDER_CHOCIES=[
        ('male',"Male"),
        ("female","Female"),
        ("other","Other")
    ]

BLOOD_GROUPS=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, null=False, default="general", choices=ROLES)
    phone_number = models.CharField(max_length=50, null=True)
    profile_image = ResizedImageField(upload_to='Profile/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    gender =  models.CharField(
        max_length=6, blank=True, null=True,
        choices=GENDER_CHOCIES,
        )
    date_of_birth = models.DateField(null=True,blank=True)
    blood_group = models.CharField(
        max_length=6, blank=True, null=True,
        choices=BLOOD_GROUPS,
        )
    location = models.ForeignKey(Unions, on_delete=models.CASCADE, blank = True , null = True)
    address = models.TextField(max_length=500, blank=True, null=False)
    def __str__(self):
        return str(self.user)
    
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.img.storage, self.img.path
        # Delete the model before the file
        super(Profile, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
    
