from django_filters import rest_framework as filters
from marketplace.models import *


# TODO: Set filter for Product
class ProductFilter(filters.FilterSet):
    pass


class ReviewFilter(filters.FilterSet):
    user_id = filters.ModelMultipleChoiceFilter(
        field_name="user_id",
        to_field_name="user_id",
        queryset=Review.objects.all())
    product_id = filters.ModelMultipleChoiceFilter(
        field_name="product_id",
        to_field_name="product_id",
        queryset=Review.objects.all()
    )
    created_at = filters.DateFilter(lookup_expr='exact')


class OrderFilter(filters.FilterSet):
    status = filters.CharFilter(lookup_expr='exact')
    summary = filters.ModelMultipleChoiceFilter(
        field_name="summary",
        to_field_name="summary",
        queryset=Order.objects.all()
    )
    created_at = filters.DateFilter(lookup_expr='exact')
    updated_at = filters.DateFilter(lookup_expr='exact')


class CompilationFilter(filters.FilterSet):
    pass
