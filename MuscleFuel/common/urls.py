from django.urls import path
from MuscleFuel.common import views
from MuscleFuel.common import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('calorie-calculator/', views.calories_calculator_funtionality, name='calorie-calculator'),
]