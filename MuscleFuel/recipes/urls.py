from os.path import pathsep
from django.urls import path
from MuscleFuel.recipes import views
from MuscleFuel.recipes.views import RecipesListView, RecipeDetailsView

urlpatterns = [
    path('', RecipesListView.as_view(), name='recipe-list'),
    path('<int:pk>/', RecipeDetailsView.as_view(), name='recipe-details'),
]
