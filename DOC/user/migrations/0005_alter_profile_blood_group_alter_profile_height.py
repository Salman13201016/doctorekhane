# Generated by Django 4.2.7 on 2024-05-30 19:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_alter_profile_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="blood_group",
            field=models.CharField(
                blank=True,
                choices=[
                    ("A+", "A+"),
                    ("A-", "A-"),
                    ("B+", "B+"),
                    ("B-", "B-"),
                    ("AB+", "AB+"),
                    ("AB-", "AB-"),
                    ("O+", "O+"),
                    ("O-", "O-"),
                ],
                max_length=6,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="height",
            field=models.CharField(blank=True, default="", max_length=50, null=True),
        ),
    ]