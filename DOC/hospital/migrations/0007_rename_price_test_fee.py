# Generated by Django 4.2.7 on 2024-03-28 10:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0006_hospital_tests"),
    ]

    operations = [
        migrations.RenameField(
            model_name="test",
            old_name="price",
            new_name="fee",
        ),
    ]
