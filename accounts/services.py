from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer,
    ActivationSerializer,
    ChangePasswordSerializer,
    ForgotPasswordCompleteSerializer,
)
from .tasks import send_activation_code_celery
from rest_framework import status
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


User = get_user_model()


class RegisterService:
    @staticmethod
    def register(data):
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return status.HTTP_201_CREATED


class ActivationService:
    @staticmethod
    def activation_post(request):
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return status.HTTP_201_CREATED

    @staticmethod
    def activation_get(email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return HttpResponse("User not found", status=400)
        user.activation_code = ""
        user.is_active = True
        user.save()


class LogoutService:
    @staticmethod
    def logout(request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordService:
    @staticmethod
    def change_password(request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        # return Response("Пароль успешно обнавлен", status=200)


class ForgotPasswordService:
    @staticmethod
    def send_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data
        email = user_data["email"]

        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()

        send_activation_code_celery(user.username, user.email, user.activation_code)
        # return Response({"Код восстановления отправлен на ваш email."}, status=status.HTTP_200_OK)


class ForgotPasswordCompleteService:
    @staticmethod
    def complete_password(request):
        serializer = ForgotPasswordCompleteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response("Пароль успешно обновлен", status=200)
