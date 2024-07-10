# Generated by Django 4.2.7 on 2024-06-20 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0002_initial'),
        ('appointment', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='testappointment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='doctorappointment',
            name='chamber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctor.chamber'),
        ),
        migrations.AddField(
            model_name='doctorappointment',
            name='doctor',
            field=models.ForeignKey(blank=True, limit_choices_to={'profile': False}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctor.doctor'),
        ),
        migrations.AddField(
            model_name='doctorappointment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentinfo',
            name='chamber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctor.chamber'),
        ),
        migrations.AddField(
            model_name='appointmentinfo',
            name='ref_doctor',
            field=models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctor.doctor'),
        ),
        migrations.AlterUniqueTogether(
            name='testappointment',
            unique_together={('user', 'test', 'hospital', 'date', 'time')},
        ),
        migrations.AlterUniqueTogether(
            name='doctorappointment',
            unique_together={('user', 'doctor', 'chamber', 'date', 'time')},
        ),
    ]