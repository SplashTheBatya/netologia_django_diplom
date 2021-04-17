from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from marketplace.views import *

router = DefaultRouter()

router.register('products', ProductViewSet)
router.register('product-reviews', ReviewViewSet)
router.register('orders', OrderViewSet)
router.register('product-collections', CompilationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls))
]
