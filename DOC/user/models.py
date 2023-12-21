from django.db import models
from app.models import District,Division,State
from django.contrib.auth.models import User
from django_resized import ResizedImageField

ROLES = [
    ('admin', 'Admin'),
    ('general', 'General'),
    ('superadmin', 'Super Admin'),
]
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
    division = models.ForeignKey(Division,on_delete=models.CASCADE,blank=True,null=True )  
    district = models.ForeignKey(District,on_delete=models.CASCADE,blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,blank=True,null=True)
    postal_code = models.IntegerField(null=True,blank=True) 
    address = models.TextField(max_length=500, blank=True, null=False)
    def __str__(self):
        return str(self.user)
    
