from os.path import pathsep
from django.urls import path
from MuscleFuel.recipes import views
from MuscleFuel.recipes.views import RecipesListView

urlpatterns = [
    path('', RecipesListView.as_view(), name='recipe-list'),
]
