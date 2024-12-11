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
        path('submit-comment/', views.comment_functionality, name='submit-comment'),
        path('edit-recipe/', views.RecipeEditView.as_view(), name='recipe-edit'),
        path('delete-recipe/', views.recipe_delete_functionality, name='recipe-delete'),
        path('delete-comment/<int:comment_pk>/', views.comment_delete_functionality, name='comment-delete'),
    ])),
    path('add-recipe/', views.RecipeAddView.as_view(), name='recipe-add')
]
