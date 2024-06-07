# Generated by Django 4.2.7 on 2024-06-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0020_alter_review_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("general", "General"),
                    ("superadmin", "Super Admin"),
                    ("doctor", "Doctor"),
                    ("hospital", "Hospital"),
                    ("ambulance", "Ambulance"),
                ],
                default="doctor",
                max_length=50,
            ),
        ),
    ]
