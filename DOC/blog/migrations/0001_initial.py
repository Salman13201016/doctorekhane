# Generated by Django 4.2.7 on 2024-03-04 20:46

import ckeditor.fields
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("content", ckeditor.fields.RichTextField(blank=True, null=True)),
                (
                    "img",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="WEBP",
                        keep_meta=True,
                        max_length=1500,
                        null=True,
                        quality=100,
                        scale=None,
                        size=[1920, 1080],
                        upload_to="blog_img/",
                    ),
                ),
                ("published", models.BooleanField(default=False)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
    ]
