from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/user_profile/', include("apps.user_profile.urls")),
    path("api/v1/recipe/", include("apps.recipe.urls")),
    path("api/v1/review/", include("apps.review.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
