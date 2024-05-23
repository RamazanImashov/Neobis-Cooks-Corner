from django.db.models import Count, Prefetch
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
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
from apps.review.serializers import LikeSerializer, FavoritesSerializer, CommentActionSerializer
from apps.review.models import Like, Favorites
from apps.user_profile.models import UserProfile
from apps.recipe.utils import delete_cache
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Create your views here.


@extend_schema(tags=['recipe'])
class RecipeViewSet(ModelViewSet):
    CACHE_KEY_PREFIX = "recipe-view"
    queryset = Recipe.objects.annotate(
        count_like=Count('likes'),
        count_favorite=Count('favorites')
    ).prefetch_related(
        "recipe_image", "recipe_ingredient", "comments", "likes", "favorites", "profile"
    )
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['difficulty', 'category']
    search_fields = ["recipe_name", "slug"]

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializers
        return RecipeDetailSerializers

    @method_decorator(cache_page(60, key_prefix=CACHE_KEY_PREFIX))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60, key_prefix=CACHE_KEY_PREFIX))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission, IsAdminPermission]
        return super().get_permissions()

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

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def favorites(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        serializer = FavoritesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            favorites = Favorites.objects.get(recipe=recipe, author=user_profile)
            favorites.delete()
            message = 'UnFavorites'
        except Favorites.DoesNotExist:
            Favorites.objects.create(recipe=recipe, author=user_profile)
            message = 'Favorites'
        return Response(message, status=200)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            like = Like.objects.get(recipe=recipe, author=user_profile)
            like.delete()
            message = 'Unlike'
        except Like.DoesNotExist:
            Like.objects.create(recipe=recipe, author=user_profile)
            message = 'Like'
        return Response(message, status=200)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        serializer = CommentActionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(recipe=recipe, author=user_profile)
            message = request.data
            return Response(message, status=200)


@extend_schema(tags=['recipe'])
class AddRecipeImageViewSet(ListCreateAPIView):
    queryset = AddRecipeImage.objects.all()
    serializer_class = AddRecipeImageSerializer


@extend_schema(tags=['recipe'])
class AddRecipeIngredientViewSet(ListCreateAPIView):
    queryset = AddRecipeIngredient.objects.all()
    serializer_class = AddRecipeIngredientSerializer
