from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from marketplace.models import Product
from marketplace.serializers import *
from marketplace.filters import *

# TODO: Set permissions
class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        pass


class ReviewViewSet(ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_permissions(self):
        pass


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_permissions(self):
        pass


class CompilationViewSet(ModelViewSet):

    queryset = Compilation.objects.all()
    serializer_class = CompilationSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = CompilationFilter

    def get_permissions(self):
        pass
