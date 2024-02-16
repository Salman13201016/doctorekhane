# Generated by Django 5.0 on 2023-12-18 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_blog_enable_json_ld_script'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='meta_author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='meta_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
