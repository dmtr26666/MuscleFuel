from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from django.db.transaction import commit
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django_filters.views import FilterView

from MuscleFuel.recipes.filters import RecipeFilter
from MuscleFuel.recipes.forms import ReviewForm, RecipeCreationForm, CommentForm, RecipeEditForm
from MuscleFuel.recipes.models import Recipe, Review, SavedRecipe


# Create your views here.
class BaseRecipeListView(FilterView, ListView):
    model = Recipe
    paginate_by = 12
    filterset_class = RecipeFilter
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = super().get_queryset()

        if type(self).__name__ == 'SavedRecipesView':
            queryset = queryset.filter(favourited_by__user=self.request.user)
        elif type(self).__name__ == 'ProfileDetailsView':
            user = self.get_object()

            queryset = queryset.filter(user=user)
            if self.request.user != user:
                queryset = queryset.filter(is_public=True)
        else:
            queryset = queryset.filter(is_public=True)

        queryset = queryset.annotate(
            average_rating=Coalesce(Avg('reviews__rating'), Value(0.0))  # Replace None with 0.0
        )

        query = self.request.GET.get('q')

        if query:
            queryset.filter(title__icontains=query)

        sort_by = self.request.GET.get('sort')
        if sort_by == 'protein_desc':
            queryset = queryset.order_by('-protein')
        elif sort_by == 'protein_asc':
            queryset = queryset.order_by('protein')
        elif sort_by == 'calories_desc':
            queryset = queryset.order_by('-calories')
        elif sort_by == 'calories_asc':
            queryset = queryset.order_by('calories')
        elif sort_by == 'rating_desc':
            queryset = queryset.order_by('-average_rating')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset


class RecipesListView(BaseRecipeListView):
    template_name = 'recipes/recipes-list.html'


class RecipeDetailsView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_macros = context['recipe'].protein + context['recipe'].carbohydrates + context['recipe'].fat

        context['protein_percentage'] = (context['recipe'].protein / total_macros) * 100 if total_macros else 0
        context['carbohydrates_percentage'] = (context['recipe'].carbohydrates / total_macros) * 100 if total_macros else 0
        context['fat_percentage'] = (context['recipe'].fat / total_macros) * 100 if total_macros else 0
        context['calories_percentage'] = (context['recipe'].calories / (context['recipe'].calories * 1.5)) * 100

        context['average_rating'] = self.object.get_average_rating()

        raw_ingredients_list = context['recipe'].ingredients.split(',')

        ingredients_list = [ingredient.strip() for ingredient in raw_ingredients_list]

        context['ingredients_list'] = ingredients_list
        context['stars_range'] = range(1, 6)

        user_review = None
        if self.request.user.is_authenticated:
            user_review = self.object.reviews.filter(user=self.request.user).first()
            self.object.is_saved = self.object.favourited_by.filter(user=self.request.user).exists()
            context['user_review'] = user_review

        context['comments'] = self.object.comments.all()

        return context

class RecipeReviewSubmit(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            recipe_id = form.cleaned_data['recipe_id']
            recipe = get_object_or_404(Recipe, id=recipe_id)

            # Prevent duplicate reviews for the same user and recipe
            review, created = Review.objects.update_or_create(
                user=request.user,
                to_recipe=recipe,
                defaults={'rating': rating},
            )

        return redirect(request.META.get('HTTP_REFERER'))

    def get(self, request, *args, **kwargs):
        return redirect('recipe-details', pk=kwargs['pk'])


class RecipeAddView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreationForm
    template_name = 'recipes/recipe-create-edit.html'

    def get_success_url(self):
        return reverse_lazy('recipe-details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user

        return super().form_valid(form)


class RecipeEditView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeEditForm
    template_name = 'recipes/recipe-create-edit.html'

    def get_success_url(self):
        return reverse_lazy('recipe-details', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_editing'] = True

        return context

@login_required
def toggle_favorite(request, pk):
    if request.POST:
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite, created = SavedRecipe.objects.get_or_create(user=request.user, to_recipe=recipe)

        if not created:
            favorite.delete()

    return redirect('recipe-details', pk=pk)


@login_required
def comment_functionality(request, pk):
    if request.POST:
        recipe = get_object_or_404(Recipe, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)

            comment.to_recipe = recipe
            comment.user = request.user
            comment.save()

    return redirect('recipe-details', pk=pk)