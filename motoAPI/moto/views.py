from django.shortcuts import render
from rest_framework import viewsets

from .models import Bike, Owner
from .serializers import BikeSerializer, OwnerSerializer


class BikeViewSet(viewsets.ModelViewSet):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
