from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify

UserModel = get_user_model()

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('BREAKFAST', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
        ('DESSERT', 'Dessert'),
        ('SNACK', 'Snack'),
        ('DRINK', 'Drink'),
    ]

    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

class Recipe(models.Model):
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
    image = CloudinaryField('image', null=False, blank=False, folder='media/recipes')
    cook_time = models.PositiveIntegerField(help_text='Cooking time in minutes.')
    servings = models.PositiveIntegerField()
    calories = models.PositiveIntegerField()
    protein = models.PositiveIntegerField()
    carbohydrates = models.PositiveIntegerField()
    fat = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name='recipes')
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

    def get_average_rating(self):
        average_rating = self.reviews.aggregate(average=Avg('rating'))['average']

        return average_rating or 0


class Review(models.Model):
    rating = models.PositiveIntegerField(null=False, blank=False)
    to_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.rating} stars"


class Comment(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['date_time_of_publication']),
        ]
        ordering = ['-date_time_of_publication']

    text = models.TextField(max_length=300)
    date_time_of_publication = models.DateTimeField(auto_now_add=True)
    to_recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='comments')


class SavedRecipe(models.Model):
    to_recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='favourited_by')
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='favourites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'to_recipe')