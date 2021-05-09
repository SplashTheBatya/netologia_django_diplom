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

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.all().filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]


class CompilationViewSet(ModelViewSet):
    queryset = Compilation.objects.all()
    serializer_class = CompilationSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = CompilationFilter

    def get_permissions(self):
        if self.action not in ["list", "retrieve"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]
