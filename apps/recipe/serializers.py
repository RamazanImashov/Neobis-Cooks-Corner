from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from apps.recipe.models import Recipe, AddRecipeImage, AddRecipeIngredient
from django.shortcuts import get_object_or_404
from apps.user_profile.models import UserProfile


class RecipeDetailSerializers(ModelSerializer):
    profile = ReadOnlyField(source="profile.username")

    class Meta:
        model = Recipe
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = AddRecipeImageSerializer(instance.recipe_image.all(), many=True).data
        rep['ingredient'] = AddRecipeIngredientSerializer(instance.recipe_ingredient.all(), many=True).data
        return rep

    def create(self, validated_data):
        user = self.context.get('request').user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return self.Meta.model.objects.create(profile=user_profile, **validated_data)


class RecipeListSerializers(ModelSerializer):
    profile = ReadOnlyField(source="profile.username")

    class Meta:
        model = Recipe
        fields = ["slug", "recipe_name", "profile"]

    # def create(self, validated_data):
    #     user = self.context.get('request').user
    #     user_profile = get_object_or_404(UserProfile, user_id=user)
    #     return self.Meta.model.objects.create(profile=user_profile, **validated_data)


class AddRecipeImageSerializer(ModelSerializer):
    class Meta:
        model = AddRecipeImage
        fields = "__all__"


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
