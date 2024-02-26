# Generated by Django 4.2.7 on 2024-02-22 21:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0002_hospital_ac_hospital_ambulance_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hospital",
            name="category",
            field=models.CharField(
                choices=[
                    ("hospital", "Hospital"),
                    ("clinic", "Clinic"),
                    ("diagnostic_center", "Diagnostic Center"),
                ],
                default="hospital",
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]