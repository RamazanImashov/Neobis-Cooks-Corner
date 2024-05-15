from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentView, RatingView, FavoriteListView

router = DefaultRouter()
router.register('comments', CommentView)
router.register('rating', RatingView)
router.register('favorites', FavoriteListView)

urlpatterns = [
    path('', include(router.urls)),
]
