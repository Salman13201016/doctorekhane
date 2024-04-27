from django.db import models
from django_resized import ResizedImageField
from django.utils.text import slugify
from unidecode import unidecode

# Create your models here.
ROLES = [
    ('admin', 'Admin'),
    ('general', 'General'),
    ('superadmin', 'Super Admin'),
    ('doctor', 'Doctor'),
    ('hospital', 'Hospital'),
]
# Create your models here.
class Divisions(models.Model):
    id = models.IntegerField(primary_key=True)
    division_name = models.CharField(max_length=50, null=False, blank=True)
    def __str__(self):
        return str(self.division_name)

class Districts(models.Model):
    division = models.ForeignKey(Divisions, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=50, null=False, blank=True)
    def __str__(self):
        return str(self.district_name)

class Upazilas(models.Model):
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    upazila_name = models.CharField(max_length=50, null=False, blank=True)
    def __str__(self):
        return str(self.upazila_name)

class Unions(models.Model):
    upazila = models.ForeignKey(Upazilas, on_delete=models.CASCADE)
    union_name = models.CharField(max_length=50, null=False, blank=True)
    def __str__(self):
        return str(self.union_name)

class Specialist(models.Model):
    specialist_name = models.CharField(max_length=100,blank=True,null=True)
    specialist_description = models.TextField(blank=True,null=True)
    specialist_logo = ResizedImageField(upload_to = 'specialist_logo/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)
    slug = models.SlugField(unique=True,blank=True, null = True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.specialist_name), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Specialist.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.specialist_logo:
            # You have to prepare what you need before delete the model
            storage, path = self.specialist_logo.storage, self.specialist_logo.path
            # Delete the model before the file
            super(Specialist, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)

class Services(models.Model):
    service_name = models.CharField(max_length=100,blank=True,null=True)
    service_description = models.TextField(blank=True,null=True)
    service_logo = ResizedImageField(upload_to = 'services_logo/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)
    slug = models.SlugField(unique=True,blank=True, null = True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.service_name), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Services.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.service_logo:
            # You have to prepare what you need before delete the model
            storage, path = self.service_logo.storage, self.service_logo.path
            # Delete the model before the file
            super(Services, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)

class Team(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    image =  ResizedImageField(upload_to = 'team_image/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)
    designation = models.CharField(max_length=100,blank=True,null=True)
    short_text = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.image:
            # You have to prepare what you need before delete the model
            storage, path = self.image.storage, self.image.path
            # Delete the model before the file
            super(Team, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)