# Generated by Django 4.2.7 on 2024-04-17 23:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointment", "0005_doctorappointment_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="testappointment",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("cancel", "Cancelled"),
                    ("done", "Done"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
    ]
