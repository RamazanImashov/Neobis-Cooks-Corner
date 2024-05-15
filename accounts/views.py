from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import LoginSerializer, ForgotPasswordSerializer, UsersSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsUserAuth
from rest_framework import generics
from django.views import View
from django.shortcuts import render
from .services import (
    RegisterService,
    ActivationService,
    LogoutService,
    ChangePasswordService,
    ForgotPasswordService,
    ForgotPasswordCompleteService,
)

# Create your views here.

User = get_user_model()


class UsersView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class RegisterView(APIView):
    service = RegisterService()

    def post(self, request):
        data = request.data
        status_code = self.service.register(data)
        return Response("Good, Registration successful", status=status_code)


class ActivationViewCode(APIView):
    service = ActivationService()

    def post(self, request):
        status_code = self.service.activation_post(request)
        return Response("Активация прошла успешно", status=status_code)


class ActivationViewDjCode(View):
    template_name = "activate.html"
    service = ActivationService()

    def get(self, request, email, activation_code):
        self.service.activation_get(email, activation_code)
        return render(request, self.template_name)


class LoginViewEmail(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = (IsUserAuth,)
    service = LogoutService()

    def post(self, request):
        response, status_code = self.service.logout(request)
        return Response(response, status=status_code)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ChangePasswordService.change_password(request=request)
        return Response("Пароль успешно обнавлен", status=200)


class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        ForgotPasswordService.send_code(self=self, request=request)
        return Response({"Код восстановления отправлен на ваш email."}, status=200)


class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        ForgotPasswordCompleteService.complete_password(request=request)
        return Response("Пароль успешно обновлен", status=200)
