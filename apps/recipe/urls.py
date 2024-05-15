from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.recipe.views import RecipeViewSet, AddRecipeImageViewSet, AddRecipeIngredientViewSet


routers = DefaultRouter()

routers.register("recipe", RecipeViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path("add_image/", AddRecipeImageViewSet.as_view()),
    path("add_ingredient/", AddRecipeIngredientViewSet.as_view()),
]
