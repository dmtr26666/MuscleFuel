from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView
from django_filters.views import FilterView

from MuscleFuel.recipes.filters import RecipeFilter
from MuscleFuel.recipes.forms import ReviewForm, RecipeCreationForm
from MuscleFuel.recipes.models import Recipe, Review


# Create your views here.
class RecipesListView(FilterView, ListView):
    model = Recipe
    template_name = 'recipes/recipes-list.html'
    context_object_name = 'recipes'
    filterset_class = RecipeFilter
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q')

        if query:
            queryset.filter(title__icontains=query)

        return queryset.order_by('-created_at').filter(is_public=True)

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

        average_rating = self.object.review_set.aggregate(average=Avg('rating'))['average']
        context['average_rating'] = average_rating or 0

        raw_ingredients_list = context['recipe'].ingredients.split(',')

        ingredients_list = [ingredient.strip() for ingredient in raw_ingredients_list]

        context['ingredients_list'] = ingredients_list
        context['stars_range'] = range(1, 6)

        user_review = None
        if self.request.user.is_authenticated:
            user_review = self.object.review_set.filter(user=self.request.user).first()
        context['user_review'] = user_review

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


class RecipeAddView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreationForm
    template_name = 'recipes/recipe-create.html'

    def get_success_url(self):
        return reverse_lazy('recipe-details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user

        return super().form_valid(form)