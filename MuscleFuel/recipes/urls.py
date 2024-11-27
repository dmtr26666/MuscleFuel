from os.path import pathsep
from django.urls import path
from MuscleFuel.recipes import views
from MuscleFuel.recipes import views

urlpatterns = [
    path('', views.RecipesListView.as_view(), name='recipe-list'),
    path('<int:pk>/', views.RecipeDetailsView.as_view(), name='recipe-details'),
    path('submit-review', views.RecipeReviewSubmit.as_view(), name='submit-review'),
]
