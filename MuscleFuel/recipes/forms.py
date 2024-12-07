from cloudinary.forms import CloudinaryFileField
from django import forms

from MuscleFuel.recipes.models import Recipe, Category, Comment


class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    recipe_id = forms.IntegerField()


class RecipeBaseForm(forms.ModelForm):
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

    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get('instance')
    #     super().__init__(*args, **kwargs)
    #
    #     if instance and instance.pk:
    #         self.fields['categories'].initial = list(instance.categories.values_list('id', flat=True))
    #
    #     print(self.fields['categories'].initial)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class RecipeCreationForm(RecipeBaseForm):
    pass


class RecipeEditForm(RecipeBaseForm):
    image = CloudinaryFileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text",]

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add comment...'}),
        }
