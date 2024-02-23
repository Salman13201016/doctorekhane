from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from django.utils.text import slugify
from unidecode import unidecode

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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.title), allow_unicode=False)
            self.slug = base_slug
            n = 1
            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(base_slug, n)
                n += 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.img.storage, self.img.path
        # Delete the model before the file
        super(Blog, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
