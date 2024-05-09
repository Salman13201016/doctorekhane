# Generated by Django 4.2.7 on 2024-03-28 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0006_hospital_tests"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("appointment", "0003_alter_doctorappointment_doctor"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestAppointment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "appointment_id",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("time", models.TimeField(blank=True, null=True)),
                ("fee", models.IntegerField(blank=True, null=True)),
                ("comment", models.TextField(blank=True, null=True)),
                ("private", models.BooleanField(default=False)),
                (
                    "hospital",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="hospital.hospital",
                    ),
                ),
                (
                    "test",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="hospital.test",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "test", "hospital", "date", "time")},
            },
        ),
    ]