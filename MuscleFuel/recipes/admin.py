from django.contrib import admin

from MuscleFuel.recipes.models import Recipe


# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'difficulty', 'is_public', 'created_at']
    filter_horizontal = ('categories',)
    list_filter = ['difficulty', 'is_public']
    search_fields = ['title', 'description', 'ingredients']
    prepopulated_fields = {'slug': ('title',)}