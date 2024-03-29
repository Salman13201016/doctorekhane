# Generated by Django 4.2.7 on 2024-03-04 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ambulance",
            name="hospital_name",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="hospital.hospital",
            ),
        ),
        migrations.AlterField(
            model_name="ambulance",
            name="hospital",
            field=models.BooleanField(default=True),
        ),
    ]
