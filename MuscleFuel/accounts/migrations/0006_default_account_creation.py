# Generated by Django 5.1.3 on 2024-12-12 13:40
from django.contrib.auth import get_user_model
from django.db import migrations

def create_default_user(apps, schema_editor):
    User = get_user_model()

    # Create a default user if it doesn't exist
    user, created = User.objects.get_or_create(email='defaultuser2@example.com', username='test_user2')
    user.set_password('somepass')
    user.save()

def reverse_create_default_user(apps, schema_editor):
    User = get_user_model()
    User.objects.filter(username='default_user').delete()  # Delete the default user if rolling back


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_options_alter_profile_bio'),
    ]

    operations = [
        migrations.RunPython(create_default_user, reverse_create_default_user),
    ]