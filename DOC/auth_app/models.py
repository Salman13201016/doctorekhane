from django.db import models

# Create your models here.
class OTP(models.Model):
    phone_number=models.CharField(max_length=20,null=True,blank=True)
    otp=models.CharField(max_length=6,null=True,blank=True)