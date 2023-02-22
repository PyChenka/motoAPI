from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import GenericViewSet

from .custom_viewset import CustomUpdateModelMixin
from .models import Bike, Owner
from .pagination import CustomPagination
from .permissions import IsSuperuserPermission
from .serializers import BikeChangeSerializer, OwnerSerializer, BikeDetailSerializer
from .throttling import NightThrottle


class BikeViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  CustomUpdateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  GenericViewSet):

    queryset = Bike.objects.all()
    throttle_classes = [UserRateThrottle, AnonRateThrottle, NightThrottle, ]
    # throttle_scope = 'low_request'
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['brand', ]
    search_fields = ['model', ]
    ordering_fields = ['made_year', ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return BikeDetailSerializer
        return BikeChangeSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'create', 'update'):
            permission_classes = [IsAuthenticated, ]
        elif self.action == 'destroy':
            permission_classes = [IsSuperuserPermission, ]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly, ]
        return [permission() for permission in permission_classes]


class OwnerViewSet(RetrieveModelMixin,
                   ListModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    throttle_classes = [UserRateThrottle, NightThrottle]
    pagination_class = CustomPagination
    # throttle_scope = 'low_request'

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsSuperuserPermission, ]
        else:
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

