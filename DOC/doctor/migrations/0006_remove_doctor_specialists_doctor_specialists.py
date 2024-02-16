# Generated by Django 4.2.7 on 2024-02-14 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0005_rename_experience_doctor_experience_year"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctor",
            name="specialists",
        ),
        migrations.AddField(
            model_name="doctor",
            name="specialists",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="doctor.specialist",
            ),
        ),
    ]
