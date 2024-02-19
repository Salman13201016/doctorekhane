# Generated by Django 4.2.7 on 2024-02-19 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hospital", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "designation",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "qualification",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "profile_image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="WEBP",
                        keep_meta=True,
                        max_length=1500,
                        null=True,
                        quality=100,
                        scale=None,
                        size=[1920, 1080],
                        upload_to="Doctor_Profile/",
                    ),
                ),
                (
                    "experience_year",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("license_no", models.CharField(blank=True, max_length=100, null=True)),
                ("slug", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("general", "General"),
                            ("superadmin", "Super Admin"),
                            ("doctor", "Doctor"),
                            ("hospital", "hospital"),
                        ],
                        default="doctor",
                        max_length=50,
                    ),
                ),
                ("address", models.TextField(blank=True, max_length=500)),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.unions",
                    ),
                ),
                (
                    "specialists",
                    models.ManyToManyField(blank=True, to="app.specialist"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Experience",
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
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "designation",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "working_place",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="experiences",
                        to="doctor.doctor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DoctorService",
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
                    "service_name",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="doctor.doctor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Chamber",
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
                ("address", models.CharField(blank=True, max_length=500, null=True)),
                ("fee", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "availability",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chamber",
                        to="doctor.doctor",
                    ),
                ),
                (
                    "hospital",
                    models.ForeignKey(
                        blank=True,
                        max_length=500,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hospital.hospital",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                    "rating",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                        null=True,
                    ),
                ),
                ("content", models.TextField(blank=True, max_length=1500, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="review",
                        to="doctor.doctor",
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
                "unique_together": {("user", "doctor")},
            },
        ),
    ]
