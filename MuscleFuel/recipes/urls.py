from os.path import pathsep
from django.urls import path, include
from MuscleFuel.recipes import views
from MuscleFuel.recipes import views

urlpatterns = [
    path('', views.RecipesListView.as_view(), name='recipe-list'),
    path('<int:pk>/', include([
        path('', views.RecipeDetailsView.as_view(), name='recipe-details'),
        path('submit-review/', views.RecipeReviewSubmit.as_view(), name='submit-review'),
        path('toggle-favourite/', views.toggle_favorite, name='toggle-favourite'),
    ])),
    path('add-recipe/', views.RecipeAddView.as_view(), name='recipe-add')
]
