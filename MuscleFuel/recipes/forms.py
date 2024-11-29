from django import forms

from MuscleFuel.recipes.models import Recipe, Category


class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    recipe_id = forms.IntegerField()


class RecipeCreationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['user', 'slug']
        labels = {
            'title': 'Recipe Title',
            'cook_time': 'Cooking Time (in minutes)',
            'description': 'Recipe description',
            'instructions': 'Cooking instructions',
            'difficulty': 'Cooking difficulty',
            'is_public': 'Make the recipe public?',
        }

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # You can use a checkbox or a select widget
        required=True,  # Make this field required
        label="Categories"
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance