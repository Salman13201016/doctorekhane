# Generated by Django 4.2.7 on 2024-02-21 11:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctor",
            name="designation",
        ),
    ]