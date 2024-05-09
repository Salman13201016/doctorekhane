# Generated by Django 4.2.7 on 2024-05-06 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0011_chamber_address_bn_chamber_availability_bn_and_more"),
        ("appointment", "0006_testappointment_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctorappointment",
            name="payment_status",
            field=models.CharField(
                choices=[("unpaid", "Unpaid"), ("paid", "Paid")],
                default="pending",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="testappointment",
            name="payment_status",
            field=models.CharField(
                choices=[("unpaid", "Unpaid"), ("paid", "Paid")],
                default="pending",
                max_length=50,
            ),
        ),
        migrations.CreateModel(
            name="AppointmentInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("invoice_id", models.CharField(blank=True, max_length=100, null=True)),
                ("patient_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "patient_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("time", models.TimeField(blank=True, null=True)),
                ("patient_age", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "patient_gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("contact_no", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "patient_type",
                    models.CharField(
                        blank=True,
                        choices=[("OPD", "Outpatient"), ("IPD", "Inpatient")],
                        max_length=3,
                        null=True,
                    ),
                ),
                (
                    "file_upload",
                    models.FileField(blank=True, null=True, upload_to="file/"),
                ),
                ("district", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "chamber",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="doctor.chamber",
                    ),
                ),
                (
                    "ref_doctor",
                    models.ForeignKey(
                        blank=True,
                        max_length=255,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="doctor.doctor",
                    ),
                ),
            ],
        ),
    ]