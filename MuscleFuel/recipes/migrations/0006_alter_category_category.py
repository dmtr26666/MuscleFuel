# Generated by Django 5.1.3 on 2024-11-28 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_category_remove_recipe_category_recipe_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=20),
        ),
    ]
