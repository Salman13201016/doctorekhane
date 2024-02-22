from django.db import models
from django_resized import ResizedImageField

# Create your models here.
ROLES = [
    ('admin', 'Admin'),
    ('general', 'General'),
    ('superadmin', 'Super Admin'),
    ('doctor', 'Doctor'),
    ('hospital', 'hospital'),
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

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.img.storage, self.img.path
        # Delete the model before the file
        super(Specialist, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)

class Services(models.Model):
    service_name = models.CharField(max_length=100,blank=True,null=True)
    service_description = models.TextField(blank=True,null=True)
    service_logo = ResizedImageField(upload_to = 'specialist_logo/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)
    
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.img.storage, self.img.path
        # Delete the model before the file
        super(Services, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)