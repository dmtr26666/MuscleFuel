from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from MuscleFuel.accounts.forms import CustomUserCreationForm

UserModel = get_user_model()

# Create your views here.

class CustomUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'

class CustomUserRegistrationView(CreateView):
    model = UserModel
    form_class = CustomUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('index')


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'
    context_object_name = 'user'