# Generated by Django 5.0 on 2024-01-03 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_hospital_hospital_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
    ]