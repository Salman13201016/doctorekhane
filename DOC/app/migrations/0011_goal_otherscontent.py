# Generated by Django 4.2.7 on 2024-05-12 18:38

import ckeditor.fields
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_notice"),
    ]

    operations = [
        migrations.CreateModel(
            name="Goal",
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
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("title_bn", models.CharField(blank=True, max_length=100, null=True)),
                ("content", models.TextField(blank=True, null=True)),
                ("content_bn", models.TextField(blank=True, null=True)),
                (
                    "icon",
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
                        upload_to="specialist_logo/",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OthersContent",
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
                (
                    "about_us_content",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "about_us_content_bn",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "termsncondition_content",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "termsncondition_content_bn",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "privacy_policy_content",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "privacy_policy_content_bn",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
            ],
        ),
    ]
