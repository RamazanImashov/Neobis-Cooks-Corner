from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.recipe.models import Recipe, AddRecipeImage, AddRecipeIngredient
from apps.recipe.serializers import (
    RecipeListSerializers,
    RecipeDetailSerializers,
    AddRecipeImageActionSerializer,
    AddRecipeImageSerializer,
    AddRecipeIngredientActionSerializer,
    AddRecipeIngredientSerializer
)
from .permissions import IsAdminPermission, IsAuthorPermission
from rest_framework.decorators import action
from apps.user_profile.models import UserProfile
from django.shortcuts import get_object_or_404

# Create your views here.


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializers
        return RecipeDetailSerializers

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def add_image(self, request, pk=None):
        recipe_id = self.get_object()
        serializer = AddRecipeImageActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(recipe_id=recipe_id)
        return Response("good", status=200)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def add_ingredient(self, request, pk=None):
        recipe_id = self.get_object()
        serializer = AddRecipeIngredientActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(recipe_id=recipe_id)
        message = request.data
        return Response(message, status=200)


class AddRecipeImageViewSet(ListCreateAPIView):
    queryset = AddRecipeImage.objects.all()
    serializer_class = AddRecipeImageSerializer


class AddRecipeIngredientViewSet(ListCreateAPIView):
    queryset = AddRecipeIngredient.objects.all()
    serializer_class = AddRecipeIngredientSerializer
