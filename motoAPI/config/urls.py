from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from moto.views import BikeViewSet, OwnerViewSet

router = DefaultRouter()
router.register('bike', BikeViewSet)
router.register('owner', OwnerViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
]
