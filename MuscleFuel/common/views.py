from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from MuscleFuel.common.forms import CalorieCalculatorForm
from MuscleFuel.recipes.models import Category


# Create your views here.

class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breakfast_id'] = Category.objects.filter(category__iexact='breakfast').first().id
        context['lunch_id'] = Category.objects.filter(category__iexact='lunch').first().id
        context['dinner_id'] = Category.objects.filter(category__iexact='dinner').first().id
        context['snack_id'] = Category.objects.filter(category__iexact='snack').first().id

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

            # Calculate BMR
            if gender == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

            # Calculate TDEE
            tdee = bmr * activity_level

            result = {
                'bmr': round(bmr, 2),
                'tdee': round(tdee, 2),
                'gain_weight': round(tdee + 500, 2),
                'lose_weight': round(tdee - 500, 2),
                'maintain_weight': round(tdee, 2),
            }
    else:
        form = CalorieCalculatorForm()

    return render(request, 'common/calorie_calculator.html', {'form': form, 'result': result})
