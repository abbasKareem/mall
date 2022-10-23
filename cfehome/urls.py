from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # path('admin_tools_stats/', include('admin_tools_stats.urls')),

    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('__debug__/', include('debug_toolbar.urls')),
    # path('forest', include('django_forest.urls')),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # api

    path('', include('api.urls')),

]
