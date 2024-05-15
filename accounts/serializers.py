from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import (
    RegisterValidator,
    ActivationValidator,
    LoginValidator,
    ChangePasswordValidator,
    ForgotPasswordValidator,
    ForgotPasswordCompleteValidator,
)


User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser', 'is_staff', 'is_active',]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate(self, attrs):
        return RegisterValidator.validate(attrs=attrs)

    def create(self, validated_data):
        return RegisterValidator.create(validated_data=validated_data)


class ActivationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        return ActivationValidator.validate(attrs=attrs)

    def activate(self):
        ActivationValidator.activate(self=self)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        return LoginValidator.validate_email(email=email)

    def validate(self, attrs):
        return LoginValidator.validate(self=self, attrs=attrs)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4, required=True)
    new_password = serializers.CharField(min_length=4, required=True)
    new_password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_old_password(self, old_password):
        return ChangePasswordValidator.validate_old_password(
            self=self, old_password=old_password
        )

    def validate(self, attrs):
        return ChangePasswordValidator.validate(attrs=attrs)

    def set_new_password(self):
        ChangePasswordValidator.set_new_password(self=self)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        return ForgotPasswordValidator.validate(attrs=attrs)

    def send_verification_email(self):
        ForgotPasswordValidator.send_verification_email(self=self)


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        return ForgotPasswordCompleteValidator.validate(attrs=attrs)

    def set_new_password(self):
        ForgotPasswordCompleteValidator.set_new_password(self=self)
