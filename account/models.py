from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.crypto import get_random_string


# Create your models here.


class UserManager(BaseUserManager):
    def _create(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Email not be not")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create(username, email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=40)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} - {self.email}"

    def create_activation_code(self):
        code = get_random_string(length=6, allowed_chars="0123456789")
        self.activation_code = code
