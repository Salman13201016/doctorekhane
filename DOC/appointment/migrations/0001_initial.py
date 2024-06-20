# Generated by Django 4.2.7 on 2024-06-20 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(blank=True, max_length=100, null=True)),
                ('patient_id', models.CharField(blank=True, max_length=100, null=True)),
                ('patient_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('patient_age', models.PositiveIntegerField(blank=True, null=True)),
                ('patient_gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=20, null=True)),
                ('patient_type', models.CharField(blank=True, choices=[('OPD', 'Outpatient'), ('IPD', 'Inpatient')], max_length=3, null=True)),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='file/')),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('fee', models.IntegerField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('patientstatus', models.CharField(choices=[('new', 'New Patient'), ('old', 'Old Patient')], max_length=50)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('cancel', 'Cancelled'), ('done', 'Done')], default='pending', max_length=50)),
                ('payment_status', models.CharField(choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')], default='pending', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TestAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('fee', models.IntegerField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('private', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('cancel', 'Cancelled'), ('done', 'Done')], default='pending', max_length=50)),
                ('payment_status', models.CharField(choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')], default='pending', max_length=50)),
            ],
        ),
    ]
