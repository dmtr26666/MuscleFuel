from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from MuscleFuel.accounts.models import Profile

UserModel = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email', 'username')


class ProfileEditForm(forms.ModelForm):
    profile_picture = CloudinaryFileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = Profile
        exclude = ('user', )