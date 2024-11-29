# Generated by Django 5.1.3 on 2024-11-28 18:28

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_review_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]