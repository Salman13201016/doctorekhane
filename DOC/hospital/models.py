from django.db import models
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from app.models import ROLES, Unions,Services,Specialist
from unidecode import unidecode

CATEGORY_CHOICES = [
('hospital', 'Hospital'),
('clinic', 'Clinic'),
('diagnostic_center', 'Diagnostic Center'),
]

class Hospital(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)
    location = models.ForeignKey(Unions, on_delete=models.CASCADE, blank = True , null = True)
    address = models.TextField(max_length=500, blank=True, null=False)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    emergency_contact = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    availability = models.CharField(max_length=500, null = True, blank = True)
    category = models.CharField(max_length=20, null = True, blank = True, choices=CATEGORY_CHOICES)
    longitude = models.CharField(max_length=100,null=True, blank=True)
    latitude = models.CharField(max_length=100,null=True, blank=True)
    specialists = models.ManyToManyField(Specialist, blank = True,)
    services = models.ManyToManyField(Services, blank = True,)
    role = models.CharField(max_length=50, null=False, default="hospital", choices=ROLES)
    slug = models.SlugField(unique=True)
    # Hospital Profile Fields
    hospital_image = ResizedImageField(upload_to='hospital/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    website = models.URLField(null=True, blank=True)

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
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.hospital_image.storage, self.hospital_image.path
        # Delete the model before the file
        super(Hospital, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
    
class Ambulance(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    hospital = models.BooleanField(default = True)
    hospital_name = models.ForeignKey(Hospital,on_delete=models.CASCADE,blank = True, null = True)
    ac = models.BooleanField(default = False)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    location = models.ForeignKey(Unions, on_delete=models.CASCADE, blank = True , null = True)
    address = models.TextField(max_length=500, blank=True, null=False)
    slug = models.SlugField(unique=True)
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
        super().save(*args, **kwargs)