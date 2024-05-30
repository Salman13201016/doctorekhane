from django.db import models
from app.models import Upazilas
# from django.contrib.auth.models import User
from django_resized import ResizedImageField
from app.models import ROLES
from django.contrib.auth.models import AbstractUser, Group, Permission

GENDER_CHOICES=[
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


class User(AbstractUser):
    role = models.CharField(max_length=50, null=False, default='general', choices=ROLES)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, null=True)
    profile_image = ResizedImageField(upload_to='Profile/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Upazilas, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=False)
    donor = models.BooleanField(blank=True, null=True, default=False)
    blood_group = models.CharField(max_length=6, blank=True, null=True, choices=BLOOD_GROUPS)
    height = models.CharField(max_length=50, blank=True, null=True, default='')
    weight = models.FloatField(blank=True, null=True)
    last_donate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def delete(self, *args, **kwargs):
        if self.profile_image:
            storage, path = self.profile_image.storage, self.profile_image.path
            super(Profile, self).delete(*args, **kwargs)
            storage.delete(path)