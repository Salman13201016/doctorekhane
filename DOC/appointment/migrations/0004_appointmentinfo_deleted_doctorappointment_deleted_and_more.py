# Generated by Django 4.0 on 2024-06-20 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentinfo',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='doctorappointment',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testappointment',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
