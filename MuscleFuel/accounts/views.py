from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from MuscleFuel.accounts.forms import CustomUserCreationForm, ProfileEditForm
from MuscleFuel.accounts.mixins import CheckUserAuthorization
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


class ProfileDetailsView(BaseRecipeListView):
    template_name = 'accounts/profile-details.html'

    def get_object(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])

        return user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        context['user_public_recipes_count'] = self.get_object().recipes.filter(is_public=True).count()
        return context

class SavedRecipesView(LoginRequiredMixin, BaseRecipeListView):
    template_name = 'accounts/saved-recipes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['saved_recipes_filter'] = True

        return context

    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])

        if user != self.request.user:
            raise PermissionDenied("You are not authorized to edit this recipe.")  # Return 403 Forbidden
        
        return super().dispatch(request, *args, **kwargs)

class ProfileEditView(LoginRequiredMixin, CheckUserAuthorization, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return self.request.user.profile.get_absolute_url()
