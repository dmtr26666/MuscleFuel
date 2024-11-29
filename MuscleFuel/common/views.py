from django.shortcuts import render
from django.views.generic import TemplateView

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