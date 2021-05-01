from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Compilation)
class CompilationAdmin(admin.ModelAdmin):
    pass


class PositionInline(admin.StackedInline):
    model = OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('user', 'product_amount')
    inlines = [PositionInline]

    def product_amount(self, obj):
        res = obj.position.all().count()
        return res


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
