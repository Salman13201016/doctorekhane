# Generated by Django 4.2.7 on 2024-05-14 23:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0015_alter_doctor_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="published",
            field=models.BooleanField(default=True),
        ),
    ]
