from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Like, Comment, Favorites
from apps.user_profile.models import UserProfile
from django.shortcuts import get_object_or_404


class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        comment = Comment.objects.create(author=user_profile, **validated_data)
        return comment


class CommentActionSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    recipe = ReadOnlyField()

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    recipe = ReadOnlyField()

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return self.Meta.model.objects.create(author=user_profile, **validated_data)


class FavoritesSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    recipe = ReadOnlyField()

    class Meta:
        model = Favorites
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return self.Meta.model.objects.create(author=user_profile, **validated_data)


class FavoritesListSerializer(ModelSerializer):
    # author = ReadOnlyField(source='author.username')

    class Meta:
        model = Favorites
        fields = '__all__'
