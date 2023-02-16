from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from .custom_viewset import CustomUpdateModelMixin
from .models import Bike, Owner
from .permissions import IsSuperuserPermission
from .serializers import BikeChangeSerializer, OwnerSerializer, BikeListSerializer, BikeDetailSerializer


class BikeViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  CustomUpdateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  GenericViewSet):

    queryset = Bike.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BikeListSerializer
        elif self.action == 'retrieve':
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

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsSuperuserPermission, ]
        else:
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

