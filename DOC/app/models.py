from django.db import models
from django_resized import ResizedImageField
from django.utils.text import slugify
from unidecode import unidecode
from ckeditor.fields import RichTextField

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


class Specialist(models.Model):
    specialist_name = models.CharField(max_length=100,blank=True,null=True)
    specialist_name_bn = models.CharField(max_length=100,blank=True,null=True)
    specialist_description = models.TextField(blank=True,null=True)
    specialist_description_bn = models.TextField(blank=True,null=True)
    specialist_logo = ResizedImageField(upload_to = 'specialist_logo/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)
    slug = models.SlugField(unique=True,blank=True, null = True)
    slug_bn = models.SlugField(unique=True,blank=True, null = True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.specialist_name), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Specialist.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        if not self.slug_bn:
            base_slug = slugify(unidecode(self.specialist_name_bn), allow_unicode=False)
            self.slug_bn = base_slug
            m = 1
            while Specialist.objects.filter(slug_bn=self.slug_bn).exists():
                self.slug_bn = '{}-{}'.format(base_slug, n)
                m += 1
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
    service_name_bn = models.CharField(max_length=100,blank=True,null=True)
    service_description_bn = models.TextField(blank=True,null=True)
    service_logo = ResizedImageField(upload_to = 'services_logo/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)
    slug = models.SlugField(unique=True,blank=True, null = True)
    slug_bn = models.SlugField(unique=True,blank=True, null = True)
    link = models.CharField(max_length=100,blank=True,null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.service_name), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Services.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        if not self.slug_bn:
            base_slug = slugify(unidecode(self.service_name_bn), allow_unicode=False)
            self.slug_bn = base_slug
            m = 1
            while Services.objects.filter(slug_bn=self.slug_bn).exists():
                self.slug_bn = '{}-{}'.format(base_slug, n)
                m += 1
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
    name_bn = models.CharField(max_length=100,blank=True,null=True)
    image =  ResizedImageField(upload_to = 'team_image/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)
    designation = models.CharField(max_length=100,blank=True,null=True)
    designation_bn = models.CharField(max_length=100,blank=True,null=True)
    short_text = models.TextField(blank=True,null=True)
    short_text_bn = models.TextField(blank=True,null=True)

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

class SiteSettings(models.Model):
    logo = ResizedImageField(upload_to='logo/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    banner = ResizedImageField(upload_to='banner/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    mail = models.EmailField(max_length=255,null = True, blank = True)
    phone = models.CharField(max_length=255,null = True, blank = True)
    whatsapp = models.CharField(max_length=255,null = True, blank = True)

class ActionLog(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} at {self.timestamp}"
    

class Notifications(models.Model):
    user = models.ForeignKey("user.User",on_delete=models.CASCADE,blank = True, null = True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Notice(models.Model):
    title = models.CharField(max_length=200,null=True,blank =  True)
    title_bn = models.CharField(max_length=200,null=True,blank =  True)
    content = models.TextField(null=True,blank =  True)
    content_bn = models.TextField(null=True,blank =  True)
    start_date = models.DateTimeField(null=True,blank =  True)
    end_date = models.DateTimeField(null=True,blank =  True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Goal(models.Model):
    title = models.CharField(max_length=100,blank=True,null=True)
    title_bn = models.CharField(max_length=100,blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    content_bn = models.TextField(blank=True,null=True)
    icon = ResizedImageField(upload_to = 'goal_icon/',max_length=1500,null=True,blank=True, force_format='WEBP', quality=100)

    def delete(self, *args, **kwargs):
        if self.icon:
            # You have to prepare what you need before delete the model
            storage, path = self.icon.storage, self.icon.path
            # Delete the model before the file
            super(Specialist, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)

class OthersContent(models.Model):
    about_us_content = RichTextField(blank=True, null=True)
    about_us_content_bn = RichTextField(blank=True, null=True)
    termsncondition_content = RichTextField(blank=True, null=True)
    termsncondition_content_bn = RichTextField(blank=True, null=True)
    privacy_policy_content = RichTextField(blank=True, null=True)
    privacy_policy_content_bn = RichTextField(blank=True, null=True)
