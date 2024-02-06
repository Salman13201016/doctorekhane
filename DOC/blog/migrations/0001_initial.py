# Generated by Django 5.0 on 2023-12-12 22:25

import ckeditor_uploader.fields
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('img', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, max_length=1500, null=True, quality=100, scale=None, size=[1920, 1080], upload_to='blog_img/')),
                ('meta_description', models.TextField()),
                ('meta_keywords', models.CharField(max_length=255)),
                ('meta_author', models.CharField(max_length=255)),
                ('meta_robot_index', models.BooleanField(default=True)),
                ('meta_robot_follow', models.BooleanField(default=True)),
                ('enable_json_ld_script', models.BooleanField(default=False)),
                ('json_ld_script', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]