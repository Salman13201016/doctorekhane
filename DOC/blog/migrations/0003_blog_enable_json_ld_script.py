# Generated by Django 5.0 on 2023-12-18 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_blog_enable_json_ld_script'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='enable_json_ld_script',
            field=models.BooleanField(default=False),
        ),
    ]
