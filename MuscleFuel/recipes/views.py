from django.shortcuts import render
from django.views.generic import ListView
from django_filters.views import FilterView

from MuscleFuel.recipes.filters import RecipeFilter
from MuscleFuel.recipes.models import Recipe


# Create your views here.
class RecipesListView(FilterView, ListView):
    model = Recipe
    template_name = 'recipes/recipes-list.html'
    context_object_name = 'recipes'
    filterset_class = RecipeFilter
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')
