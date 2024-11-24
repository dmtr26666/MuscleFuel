import django_filters
from .models import Recipe

class RecipeFilter(django_filters.FilterSet):
    cook_time = django_filters.RangeFilter()
    category = django_filters.ChoiceFilter(choices=Recipe.CATEGORY_CHOICES, empty_label='All Categories')
    difficulty = django_filters.ChoiceFilter(choices=Recipe.DIFFICULTY_CHOICES, empty_label='All Difficulties')

    class Meta:
        model = Recipe
        fields = ['category', 'difficulty', 'cook_time']
