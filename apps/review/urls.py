from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentView, FavoriteListView


router = DefaultRouter()
router.register("favorite", FavoriteListView)


urlpatterns = [
    path("", include(router.urls)),
    # path('favorites/', FavoriteListView.as_view(), name='favorites_list'),
    path("comments/", CommentView.as_view(), name="comments_list")
]
