from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('BREAKFAST', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
        ('DESSERT', 'Dessert'),
        ('SNACK', 'Snack'),
        ('DRINK', 'Drink'),
    ]

    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    ingredients = models.TextField(help_text='List ingredients, separated by commas.')
    instructions = models.TextField(help_text='Step-by-step preparation instructions.')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    cook_time = models.PositiveIntegerField(help_text='Cooking time in minutes.')
    servings = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
