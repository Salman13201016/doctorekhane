# Generated by Django 4.2.7 on 2024-02-23 00:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0005_alter_hospital_ac"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hospital",
            name="ac",
            field=models.BooleanField(default=False),
        ),
    ]
