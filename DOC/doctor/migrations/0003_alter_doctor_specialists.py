# Generated by Django 5.0 on 2024-02-03 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_doctor_license_no_doctor_qualification_doctor_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='specialists',
            field=models.ManyToManyField(blank=True, to='doctor.specialist'),
        ),
    ]