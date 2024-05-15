from .models import Like, Dislike, Comment, Rating
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import generics
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from .perimissions import IsAuthor


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


class CommentView(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RatingView(PermissionMixin, ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class FavoriteListView(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesListSerializer

    def get_queryset(self):
        return Favorites.objects.filter(author=self.request.user)



