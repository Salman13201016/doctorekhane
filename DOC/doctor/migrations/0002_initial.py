# Generated by Django 4.2.7 on 2024-03-04 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("doctor", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("hospital", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="chamber",
            name="doctor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chamber",
                to="doctor.doctor",
            ),
        ),
        migrations.AddField(
            model_name="chamber",
            name="hospital",
            field=models.ForeignKey(
                blank=True,
                max_length=500,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="hospital.hospital",
            ),
        ),
    ]
