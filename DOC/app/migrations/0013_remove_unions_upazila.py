# Generated by Django 4.2.7 on 2024-05-17 23:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0012_alter_goal_icon"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="unions",
            name="upazila",
        ),
    ]
