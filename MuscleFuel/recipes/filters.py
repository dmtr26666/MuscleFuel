import django_filters

from .models import Recipe

class RecipeFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_by_query', label='Title')
    cook_time = django_filters.RangeFilter()
    category = django_filters.ChoiceFilter(choices=Recipe.CATEGORY_CHOICES, empty_label='All Categories')
    difficulty = django_filters.ChoiceFilter(choices=Recipe.DIFFICULTY_CHOICES, empty_label='All Difficulties')

    class Meta:
        model = Recipe
        fields = ['q', 'category', 'difficulty', 'cook_time']

    def filter_by_query(self, queryset, name, value):
        return queryset.filter(
            title__icontains=value
        )

