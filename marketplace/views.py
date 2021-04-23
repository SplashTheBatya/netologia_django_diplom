from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet
from marketplace.permissions import *

from marketplace.serializers import *
from marketplace.filters import *


# TODO: Rework, add custom filter
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    # TODO: Reformat permissions
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    # TODO: Reformat permissions
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAdminUser(), IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwner(), IsAdminUser()]
        else:
            return [AllowAny()]


# TODO: Try and rework
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    # TODO: Reformat permissions
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["list", "retrieve", "update"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]


class CompilationViewSet(ModelViewSet):
    queryset = Compilation.objects.all()
    serializer_class = CompilationSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = CompilationFilter

    # TODO: Reformat permissions
    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]
