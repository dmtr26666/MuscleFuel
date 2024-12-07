from django.urls import path, include
from MuscleFuel.accounts import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.CustomUserRegistrationView.as_view(), name='register'),
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailsView.as_view(), name='profile-details'),
        path('saved-recipes/', views.SavedRecipesView.as_view(), name='user-saved-recipes'),
        path('edit/', views.ProfileEditView.as_view(), name='edit-profile'),
    ])),
]