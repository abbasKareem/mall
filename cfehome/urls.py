from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib import admin
from django.urls import re_path, path, include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from rest_framework.routers import DefaultRouter
from api.views import UserviewSet


router = DefaultRouter()
router.register('user', UserviewSet, basename='user')


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    url('', include('pwa.urls')),


    path('', include('api.urls')),

]

urlpatterns += router.urls
