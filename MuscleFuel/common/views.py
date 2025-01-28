from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from MuscleFuel.common.forms import CalorieCalculatorForm
from MuscleFuel.recipes.models import Category, Recipe


# Create your views here.

class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breakfast_id'] = Category.objects.filter(category__iexact='breakfast').first().id
        context['lunch_id'] = Category.objects.filter(category__iexact='lunch').first().id
        context['dinner_id'] = Category.objects.filter(category__iexact='dinner').first().id
        context['snack_id'] = Category.objects.filter(category__iexact='snack').first().id

        context['all_recipes'] = Recipe.objects.all()[:10]

        return context


def calories_calculator_funtionality(request):
    result = None

    if request.method == "POST":
        form = CalorieCalculatorForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            gender = form.cleaned_data['gender']
            activity_level = float(form.cleaned_data['activity_level'])
            goal = form.cleaned_data['goal']

            # Calculate BMR
            if gender == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

            # Calculate TDEE
            tdee = bmr * activity_level

            if goal == 'gain':
                tdee += 400  # Calorie surplus for muscle gain
                macros_ratio = {'protein': 0.3, 'carbs': 0.4, 'fats': 0.3}
            elif goal == 'lose':
                tdee -= 400  # Calorie deficit for fat loss
                macros_ratio = {'protein': 0.35, 'carbs': 0.35, 'fats': 0.3}
            else:
                macros_ratio = {'protein': 0.3, 'carbs': 0.4, 'fats': 0.3}

            # Calculate macronutrient grams
            protein_grams_1 = (tdee * macros_ratio['protein']) / 4
            protein_grams_2 = weight * 2.2
            carbs_grams = (tdee * macros_ratio['carbs']) / 4
            fats_grams = (tdee * macros_ratio['fats']) / 9

            result = {
                'bmr': round(bmr, 2),
                'tdee': round(tdee, 2),
                'goal': goal.title(),
                'protein1': round(protein_grams_1, 2),
                'protein2': round(protein_grams_2, 2),
                'carbs': round(carbs_grams, 2),
                'fats': round(fats_grams, 2),
            }
    else:
        form = CalorieCalculatorForm()

    return render(request, 'common/calorie_calculator.html', {'form': form, 'result': result})
