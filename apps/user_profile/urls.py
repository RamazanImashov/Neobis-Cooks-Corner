from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ToggleSubscriptionAPIView, SubscriptionsListView, FollowersListView

routers = DefaultRouter()
routers.register('profile', ProfileViewSet)

urlpatterns = [
    path('toggle-subscription/<int:user_id>/', ToggleSubscriptionAPIView.as_view(), name='toggle_subscription'),
    path('subscriptions/', SubscriptionsListView.as_view(), name='subscriptions_list'),
    path('followers/', FollowersListView.as_view(), name='followers_list'),
    path('', include(routers.urls)),
]
