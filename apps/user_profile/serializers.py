from rest_framework import serializers
from apps.user_profile.models import UserProfile
from django.contrib.auth import get_user_model
from apps.recipe.serializers import RecipeDetailSerializers, RecipeListSerializers


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.email')
    followers_count = serializers.SerializerMethodField()
    subscriptions_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_subscriptions_count(self, obj):
        return obj.subscriptions.count()

    def validate(self, data):
        current_user = self.context.get("request").user
        if self.instance and self.instance.user != current_user:
            raise serializers.ValidationError("You cannot modify another user's profile")
        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["recipe"] = RecipeListSerializers(instance.recipe.all(), many=True).data
        return rep

    def create(self, validated_data):
        user = self.context['request'].user
        return self.Meta.model.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance


class UserSubscriptionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ("id", 'username', 'profile_image')

    def get_username(self, obj):
        return f"{obj.username}"
