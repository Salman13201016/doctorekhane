# Generated by Django 5.0 on 2024-01-06 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0008_alter_hospital_accreditation_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='latitude',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='longitude',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
