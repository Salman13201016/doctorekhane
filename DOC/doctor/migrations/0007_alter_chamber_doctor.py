# Generated by Django 4.2.7 on 2024-03-21 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0006_review"),
    ]

    operations = [
        migrations.AlterField(
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
    ]