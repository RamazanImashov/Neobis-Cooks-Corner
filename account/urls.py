from django.urls import path, include
from .views import (
    RegisterView,
    ActivationViewCode,
    LogoutView,
    ChangePasswordView,
    ForgotPasswordView,
    ForgotPasswordCompleteView,
    ActivationViewDjCode,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # path('users/', UsersView.as_view({'get': 'list'})),
    path("register/", RegisterView.as_view()),
    path(
        "activate/<str:email>/<str:activation_code>/",
        ActivationViewDjCode.as_view(),
        name="activate",
    ),
    path("activate_code/", ActivationViewCode.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("change_password/", ChangePasswordView.as_view()),
    path("lose_password/", ForgotPasswordView.as_view()),
    path("lose_confirm_code/", ForgotPasswordCompleteView.as_view(), name="forgot"),
]
