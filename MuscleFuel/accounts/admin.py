from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from MuscleFuel.accounts.forms import CustomUserCreationForm, CustomUserChangeForm

UserModel = get_user_model()

# Register your models here.
@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = UserModel
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('pk', 'email', 'username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )