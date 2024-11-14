from django.urls import path
from MuscleFuel.accounts import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.CustomUserRegistrationView.as_view(), name='register'),
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]