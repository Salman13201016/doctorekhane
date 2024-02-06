from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField

class Blog(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    content = RichTextField(blank=True, null=True)
    img = ResizedImageField(upload_to='blog_img/', max_length=1500, null=True, blank=True, force_format='WEBP', quality=100)
    published = models.BooleanField(default = False)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title
