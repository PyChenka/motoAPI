from rest_framework.mixins import *
from rest_framework.viewsets import GenericViewSet

from .custom_viewset import CustomUpdateModelMixin
from .models import Bike, Owner
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


class OwnerViewSet(RetrieveModelMixin,
                   ListModelMixin,
                   GenericViewSet):

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
