from django.db import migrations, transaction
from django.utils.text import slugify
from django.contrib.auth import get_user_model  # Import get_user_model dynamically

from MuscleFuel.accounts.models import CustomUser


def populate_initial_data(apps, schema_editor):
    # Get the custom User model dynamically using get_user_model()
    User = get_user_model()
    Category = apps.get_model('recipes', 'Category')

    with transaction.atomic():  # Ensure atomic transactions for safety

        # Populate categories
        categories = ['BREAKFAST', 'LUNCH', 'DINNER', 'DESSERT', 'SNACK', 'DRINK']
        category_objects = {}
        for category_name in categories:
            obj, _ = Category.objects.get_or_create(category=category_name)
            category_objects[category_name] = obj


def reverse_initial_data(apps, schema_editor):
    # Undo data creation
    Category = apps.get_model('recipes', 'Category')

    Category.objects.filter(category__in=['BREAKFAST', 'LUNCH', 'DINNER', 'DESSERT', 'SNACK', 'DRINK']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0011_alter_recipe_image'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data, reverse_initial_data),
    ]
