from django_filters import rest_framework as filters
from marketplace.models import *


# TODO: Set filter for Product
class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()
    description = filters.CharFilter(lookup_expr='contains')
    name = filters.CharFilter(lookup_expr='exact')


class ReviewFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        field_name="user_id",
        to_field_name="user_id",
        queryset=Review.objects.all())
    product = filters.ModelMultipleChoiceFilter(
        field_name="product_id",
        to_field_name="product_id",
        queryset=Review.objects.all()
    )
    created_at = filters.DateFromToRangeFilter(lookup_expr='exact')
    updated_at = filters.DateFromToRangeFilter(lookup_expr='exact')


class OrderFilter(filters.FilterSet):
    status = filters.CharFilter(lookup_expr='exact')
    summary = filters.RangeFilter()
    created_at = filters.DateFromToRangeFilter(lookup_expr='exact')
    updated_at = filters.DateFromToRangeFilter(lookup_expr='exact')


class CompilationFilter(filters.FilterSet):
    pass
