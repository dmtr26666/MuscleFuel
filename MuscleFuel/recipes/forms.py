from PIL import Image
from cloudinary import CloudinaryResource
from cloudinary.forms import CloudinaryFileField
from django import forms
from django.core.exceptions import ValidationError

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

    image = CloudinaryFileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if isinstance(image, CloudinaryResource):
                return image

            try:
                img = Image.open(image)
                img.verify()

            except (IOError, SyntaxError) as e:
                raise ValidationError("The uploaded file is not a valid image.")

        return image


class RecipeCreationForm(RecipeBaseForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Recipe.objects.filter(title__iexact=title).exists():
            raise ValidationError("A recipe with this title already exists. Please choose a different title.")

        return title


class RecipeEditForm(RecipeBaseForm):
    pass


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text",]

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add comment...'}),
        }
