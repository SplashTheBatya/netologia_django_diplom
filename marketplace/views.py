from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet
from marketplace.permissions import *

from marketplace.serializers import *
from marketplace.filters import *


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ["post", "create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwner()]
        else:
            return [AllowAny()]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    # TODO: Add list method, maybe else method
    def list(self, request, *args, **kwargs):
        if self.action in ["list"]:
            if IsAdminUser():
                return super().list(request)
            else:
                queryset = self.filter_queryset(self.get_queryset())
                queryset.filter()

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["list", "partial_update", "update"]:
            return [IsAdminUser()]
        elif self.action in ["retrieve"]:
            return [IsOwner(), IsAdminUser()]


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
