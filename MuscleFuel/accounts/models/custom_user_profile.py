from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

UserModel = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = CloudinaryField('image', null=True, blank=True, folder='media/profile_pics')
    bio = models.TextField(max_length=250, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name

        return self.first_name or self.last_name or "Anonymous"

    def __str__(self):
        return f"{self.user.email}'s Profile"

    def get_absolute_url(self):
        return reverse('profile-details', kwargs={'pk': self.pk})