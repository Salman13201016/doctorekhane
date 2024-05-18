# Generated by Django 4.2.7 on 2024-05-17 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0013_remove_unions_upazila"),
        ("hospital", "0015_test_description_test_description_bn_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ambulance",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.upazilas",
            ),
        ),
        migrations.AlterField(
            model_name="hospital",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.upazilas",
            ),
        ),
    ]
