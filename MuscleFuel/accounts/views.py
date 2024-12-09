from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from MuscleFuel.accounts.forms import CustomUserCreationForm, ProfileEditForm
from MuscleFuel.accounts.models import Profile
from MuscleFuel.recipes.views import BaseRecipeListView

UserModel = get_user_model()

# Create your views here.

class CustomUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'

class CustomUserRegistrationView(CreateView):
    model = UserModel
    form_class = CustomUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('index')


class ProfileDetailsView(DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'
    context_object_name = 'user'


class SavedRecipesView(LoginRequiredMixin, BaseRecipeListView):
    template_name = 'accounts/saved-recipes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['saved_recipes_filter'] = True

        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return self.request.user.profile.get_absolute_url()

    def get_object(self, queryset=None):
        return self.request.user.profile