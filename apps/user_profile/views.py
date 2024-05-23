
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, Http404
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Count, Subquery, OuterRef
from apps.recipe.models import Recipe
from accounts.serializers import UsersSerializer
from .permissions import IsAdminPermission, IsAuthorPermission
from apps.user_profile.models import UserProfile
from apps.user_profile.serializers import ProfileSerializer, UserSubscriptionSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from apps.user_profile.utils import delete_cache

User = get_user_model()


@extend_schema(tags=['profile'])
class ProfileViewSet(viewsets.ModelViewSet):
    CACHE_KEY_PREFIX = "profile-view"
    queryset = UserProfile.objects.annotate(
        followers_count=Count('followers'),
        subscriptions_count=Count('subscriptions')
    ).only('username', 'description', 'profile_image').prefetch_related(
        "recipe__recipe_image", "recipe__recipe_ingredient",
        "recipe__comments", "recipe__likes", "recipe__favorites"
    )
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ["username"]

    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    @method_decorator(cache_page(60, key_prefix=CACHE_KEY_PREFIX))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60, key_prefix=CACHE_KEY_PREFIX))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


@extend_schema(tags=['profile'])
class ToggleSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        if request.user.id == user_id:
            return Response({"error": "Cannot subscribe to or unsubscribe from self."}, status=status.HTTP_400_BAD_REQUEST)

        target_user = get_object_or_404(User, id=user_id)
        target_profile = get_object_or_404(UserProfile, user_id=target_user)

        user_profile = get_object_or_404(UserProfile, user_id=request.user)

        if target_profile in user_profile.subscriptions.all():
            user_profile.subscriptions.remove(target_profile)
            return Response({"message": "Unsubscribed successfully."}, status=status.HTTP_200_OK)
        else:
            user_profile.subscriptions.add(target_profile)
            return Response({"message": "Subscribed successfully."}, status=status.HTTP_200_OK)


@extend_schema(tags=['profile'])
class SubscriptionsListView(ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return user_profile.subscriptions.all()


@extend_schema(tags=['profile'])
class FollowersListView(ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return user_profile.followers.all()
