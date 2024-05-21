from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError, SerializerMethodField
from apps.recipe.models import Recipe, AddRecipeImage, AddRecipeIngredient
from django.shortcuts import get_object_or_404
from apps.user_profile.models import UserProfile
from apps.review.serializers import CommentSerializer, FavoritesListSerializer


class RecipeDetailSerializers(ModelSerializer):
    profile = ReadOnlyField(source="profile.username")
    count_like = SerializerMethodField('get_count_like')
    count_favorite = SerializerMethodField("get_favorite")
    ingredient = SerializerMethodField("get_ingredient")
    images = SerializerMethodField("get_image")


    class Meta:
        model = Recipe
        fields = ["slug", "recipe_name", "profile",
                  "count_like", "count_favorite",
                  "description", "difficulty",
                  "category", 'preparation_time', "ingredient", "images"]

    def get_count_like(self, obj):
        return obj.likes.count()

    def get_favorite(self, obj):
        return obj.favorites.count()

    def get_image(self, obj):
        return AddRecipeImageSerializer(obj.recipe_image.all(), many=True).data

    def get_ingredient(self, obj):
        return AddRecipeIngredientSerializer(obj.recipe_ingredient.all(), many=True).data

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data

    def create(self, validated_data):
        user = self.context.get('request').user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return self.Meta.model.objects.create(profile=user_profile, **validated_data)


class RecipeListSerializers(ModelSerializer):
    images = SerializerMethodField("get_image")
    count_like = SerializerMethodField('get_count_like')
    count_favorite = SerializerMethodField("get_count_favorite")

    class Meta:
        model = Recipe
        fields = ["slug", "recipe_name", "profile", "count_like", "count_favorite", "images"]

    def get_count_like(self, obj):
        return obj.likes.count()

    def get_count_favorite(self, obj):
        return obj.favorites.count()

    def get_image(self, obj):
        return AddRecipeImageSerializer(obj.recipe_image.all(), many=True).data


class AddRecipeImageSerializer(ModelSerializer):
    class Meta:
        model = AddRecipeImage
        fields = ["image", ]


class AddRecipeImageActionSerializer(ModelSerializer):
    recipe_id = ReadOnlyField()

    class Meta:
        model = AddRecipeImage
        fields = '__all__'

    def create(self, validated_data):
        return AddRecipeImage.objects.create(**validated_data)


class AddRecipeIngredientSerializer(ModelSerializer):
    class Meta:
        model = AddRecipeIngredient
        fields = "__all__"


class AddRecipeIngredientActionSerializer(ModelSerializer):
    recipe_id = ReadOnlyField()

    class Meta:
        model = AddRecipeIngredient
        fields = '__all__'

    def create(self, validated_data):
        return AddRecipeIngredient.objects.create(**validated_data)
