from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from moto.views import BikeViewSet, OwnerViewSet

router = DefaultRouter()
router.register('bikes', BikeViewSet)
router.register('owners', OwnerViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),

]
