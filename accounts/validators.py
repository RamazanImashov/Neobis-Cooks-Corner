from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model, authenticate
from .tasks import send_password_celery, send_activation_code_celery
from rest_framework import serializers


User = get_user_model()


class RegisterValidator:
    @staticmethod
    def validate(attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise ValidationError("Password not confirm")
        return attrs

    @staticmethod
    def create(validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery(user.username, user.email, user.activation_code)
        return user


class ActivationValidator:
    @staticmethod
    def validate(attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        code = attrs.get("code")
        if not User.objects.filter(
            username=username, email=email, activation_code=code
        ).exists():
            raise serializers.ValidationError("Пользователь не найден")
        return attrs

    @staticmethod
    def activate(self):
        username = self.validated_data.get("username")
        user = User.objects.get(username=username)
        user.is_active = True
        user.activation_code = ""
        user.save()


class LoginValidator:
    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise ValidationError("User not found")
        return email

    @staticmethod
    def validate(self, attrs):
        request = self.context.get("request")
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(username=email, password=password, request=request)

            if not user:
                raise ValidationError("Error email or password")

        else:
            raise ValidationError("Username and password obazatelno")

        attrs["user"] = user
        return attrs


class ChangePasswordValidator:
    @staticmethod
    def validate_old_password(self, old_password):
        request = self.context.get("request")
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Введите корректный пароль")
        return old_password

    @staticmethod
    def validate(attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError("Пароли не совпадают")
        if new_password == old_password:
            raise serializers.ValidationError("Старый и новый пароли совпадают")
        return attrs

    @staticmethod
    def set_new_password(self):
        new_password = self.validated_data.get("new_password")
        user = self.context.get("request").user
        user.set_password(new_password)
        user.save()


class ForgotPasswordValidator:
    @staticmethod
    def validate(attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден")
        return attrs

    @staticmethod
    def send_verification_email(self):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_password_celery(user.username, user.email, user.activation_code)


class ForgotPasswordCompleteValidator:
    @staticmethod
    def validate(attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")

        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError(
                "Пользователь не найден или неправильный код"
            )
        if password != password_confirm:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    @staticmethod
    def set_new_password(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ""
        user.save()
