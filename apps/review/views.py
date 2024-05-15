from .models import Comment, Favorites
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import generics
from .serializers import CommentSerializer, FavoritesListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .perimissions import IsAuthor
from apps.user_profile.models import UserProfile
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

# Create your views here.

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permissions = [IsAuthor]
        else:
            permissions = [AllowAny]
        return [permissions() for permissions in permissions]


@extend_schema(tags=['review'])
class CommentView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@extend_schema(tags=['review'])
class FavoriteListView(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesListSerializer

    def get_queryset(self):
        user = self.request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        favorite = Favorites.objects.filter(author=user_profile)
        return favorite
