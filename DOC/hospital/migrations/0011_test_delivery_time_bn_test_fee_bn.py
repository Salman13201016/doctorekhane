# Generated by Django 4.2.7 on 2024-05-01 21:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0010_ambulance_address_bn_ambulance_name_bn_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="test",
            name="delivery_time_bn",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="test",
            name="fee_bn",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
