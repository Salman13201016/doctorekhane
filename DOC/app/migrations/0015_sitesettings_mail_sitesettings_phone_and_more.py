# Generated by Django 4.2.7 on 2024-05-28 21:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0014_delete_unions"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="mail",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="phone",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="whatsapp",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
