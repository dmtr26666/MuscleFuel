import django_filters
from django import forms

from .models import Recipe, Category


class RecipeFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_by_query', label='Title')
    cook_time = django_filters.RangeFilter()
    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Categories',
    )
    difficulty = django_filters.ChoiceFilter(choices=Recipe.DIFFICULTY_CHOICES, empty_label='All Difficulties')

    class Meta:
        model = Recipe
        fields = ['q', 'categories', 'difficulty', 'cook_time']

    def filter_by_query(self, queryset, name, value):
        return queryset.filter(
            title__icontains=value
        )

