# Generated by Django 4.2.7 on 2024-05-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0011_chamber_address_bn_chamber_availability_bn_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="position",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
