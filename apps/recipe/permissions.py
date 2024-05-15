from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from apps.user_profile.models import UserProfile


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return user_profile


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_active or request.user.is_staff)
