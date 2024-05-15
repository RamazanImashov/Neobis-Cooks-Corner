from django.contrib import admin
from apps.recipe.models import Recipe

# Register your models here.


@admin.register(Recipe)
class UserAdmin(admin.ModelAdmin):
    list_display = ["slug", "profile", "recipe_name", ]
