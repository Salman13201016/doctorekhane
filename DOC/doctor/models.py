from django.db import models
from django_resized import ResizedImageField
# from django.contrib.auth.models import User
from user.models import User
from app.models import ROLES, Unions,Specialist
from hospital.models import Hospital
from django.utils.text import slugify
from unidecode import unidecode


# Create your models here.
GENDER_CHOCIES=[
        ('male',"Male"),
        ("female","Female"),
        ("other","Other")
    ]
RATING_TYPE_CHOICES=[
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
]
            
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null = True, blank = True)
    email = models.EmailField(max_length=100, null = True, blank = True)
    qualification = models.CharField(max_length=500, null = True, blank = True)
    profile_image = ResizedImageField(upload_to='Doctor_Profile/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    experience_year = models.CharField(max_length=100, null = True, blank = True)
    specialists = models.ManyToManyField(Specialist, blank = True,)
    license_no = models.CharField(max_length=100, null = True, blank = True)
    slug = models.CharField(max_length=100, null = True, blank = True)
    role = models.CharField(max_length=50, null=False, default="doctor", choices=ROLES)
    location = models.ForeignKey(Unions, on_delete=models.CASCADE, blank = True , null = True)
    address = models.TextField(max_length=500, blank=True, null=False)
    phone_number = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOCIES)
    profile = models.BooleanField(default = False)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.name), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Doctor.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.profile_image.storage, self.profile_image.path
        # Delete the model before the file
        super(Doctor, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
    
class Chamber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='chamber', null=True, blank=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE, max_length=500, null = True, blank = True)
    fee = models.CharField(max_length=500, null = True, blank = True)
    availability = models.CharField(max_length=500, null = True, blank = True)
    personal = models.BooleanField(default=False)
    name = models.CharField(max_length=500, null = True, blank = True)
    address = models.CharField(max_length=500, null = True, blank = True)

    def __str__(self):
        return str(self.hospital.name) if self.hospital else self.name

class Experience(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='experiences', null = True, blank = True)
    start_date = models.DateField(null = True, blank = True)
    end_date = models.DateField(null = True, blank = True)
    designation = models.CharField(max_length=500, null = True, blank = True)
    working_place = models.CharField(max_length=500, null = True, blank = True)

    def __str__(self):
        return self.working_place
    
class DoctorService(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='services', null = True, blank = True)
    service_name = models.CharField(max_length=500, null = True, blank = True)

    def __str__(self):
        return self.service_name

class Review(models.Model):
    user = models.ForeignKey(User, null=True,on_delete=models.SET_NULL,blank=True)
    appointment = models.ForeignKey("appointment.DoctorAppointment", on_delete=models.CASCADE,null=True,blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='review',null=True,blank=True)
    rating=models.IntegerField(choices=RATING_TYPE_CHOICES,blank=True,null=True)
    content = models.TextField(max_length=1500,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'doctor',"appointment")