
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, Http404
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from accounts.serializers import UsersSerializer
from .permissions import IsAdminPermission, IsAuthorPermission
from apps.user_profile.models import UserProfile
from apps.user_profile.serializers import ProfileSerializer, UserSubscriptionSerializer
from rest_framework.response import Response

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        serializer = UsersSerializer(user)
        return Response(serializer.data)


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


class SubscriptionsListView(ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return user_profile.subscriptions.all()


class FollowersListView(ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_profile = get_object_or_404(UserProfile, user_id=user)
        return user_profile.followers.all()
