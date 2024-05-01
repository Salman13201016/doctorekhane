from django.db import models
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from app.models import ROLES, Unions,Services,Specialist
from unidecode import unidecode
from user.models import User

CATEGORY_CHOICES = [
('hospital', 'Hospital'),
('clinic', 'Clinic'),
('diagnostic_center', 'Diagnostic Center'),
]

class TestCatagory(models.Model):
    name = models.CharField(max_length=100,null = True, blank= True)
    name_bn = models.CharField(max_length=100,null = True, blank= True)

    def __str__(self):
        return str(self.name)

class Test(models.Model):
    catagory = models.ForeignKey(TestCatagory,on_delete=models.CASCADE,null = True, blank = True)
    test_name = models.CharField(max_length=200,null=True,blank= True)
    test_name_bn = models.CharField(max_length=200,null=True,blank= True)
    fee = models.CharField(max_length=200,null=True,blank= True)
    delivery_time = models.CharField(max_length=200,null=True,blank= True)
    slug = models.CharField(max_length=200,null=True,blank=True)
    slug_bn = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self): 
        return str(self.test_name)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.test_name), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Test.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        if not self.slug_bn:
            base_slug = slugify(unidecode(self.test_name_bn), allow_unicode=False)
            self.slug_bn = base_slug
            m = 1
            while Test.objects.filter(slug_bn=self.slug_bn).exists():
                self.slug_bn = '{}-{}'.format(base_slug, n)
                m += 1
        super().save(*args, **kwargs)

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    name_bn = models.CharField(max_length=255,null=True, blank=True)
    location = models.ForeignKey(Unions, on_delete=models.CASCADE, blank = True , null = True)
    address = models.TextField(max_length=500, blank=True, null=False)
    address_bn = models.TextField(max_length=500, blank=True, null=False)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    emergency_contact = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    description_bn = models.TextField(null=True, blank=True)
    availability = models.CharField(max_length=500, null = True, blank = True)
    availability_bn = models.CharField(max_length=500, null = True, blank = True)
    category = models.CharField(max_length=20, null = True, blank = True, choices=CATEGORY_CHOICES)
    longitude = models.CharField(max_length=100,null=True, blank=True)
    latitude = models.CharField(max_length=100,null=True, blank=True)
    specialists = models.ManyToManyField(Specialist, blank = True)
    services = models.ManyToManyField("HospitalService", blank = True,)
    tests = models.ManyToManyField(Test,blank=True)
    role = models.CharField(max_length=50, null=False, default="hospital", choices=ROLES)
    slug = models.SlugField(unique=True)
    slug_bn = models.SlugField(unique=True,blank = True,null = True)
    # Hospital Profile Fields
    hospital_image = ResizedImageField(upload_to='hospital/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    website = models.URLField(null=True, blank=True)
    profile = models.BooleanField(default = False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.name), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Hospital.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        if not self.slug_bn:
            base_slug = slugify(unidecode(self.name_bn), allow_unicode=False)
            self.slug_bn = base_slug
            m = 1
            while Hospital.objects.filter(slug_bn=self.slug_bn).exists():
                self.slug_bn = '{}-{}'.format(base_slug, n)
                m += 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.hospital_image:
            # You have to prepare what you need before delete the model
            storage, path = self.hospital_image.storage, self.hospital_image.path
            # Delete the model before the file
            super(Hospital, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)

class HospitalService(models.Model):
    service_name = models.CharField(max_length=500, null = True, blank = True)
    service_name_bn = models.CharField(max_length=500, null = True, blank = True)

    def __str__(self):
        return self.service_name

class Ambulance(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    name_bn = models.CharField(max_length=100,null=True, blank=True)
    hospital = models.BooleanField(default = True)
    hospital_name = models.ForeignKey(Hospital,on_delete=models.CASCADE,blank = True, null = True)
    ac = models.BooleanField(default = False)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    location = models.ForeignKey(Unions, on_delete=models.CASCADE, blank = True , null = True)
    address = models.TextField(max_length=500, blank=True, null=False)
    address_bn = models.TextField(max_length=500, blank=True, null=False)
    slug = models.SlugField(unique=True)
    slug_bn = models.SlugField(unique=True,blank = True, null =True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.name), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Ambulance.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        if not self.slug_bn:
            base_slug = slugify(unidecode(self.name_bn), allow_unicode=False)
            self.slug_bn = base_slug
            m = 1
            while Ambulance.objects.filter(slug_bn=self.slug_bn).exists():
                self.slug_bn = '{}-{}'.format(base_slug, n)
                m += 1
        super().save(*args, **kwargs)
