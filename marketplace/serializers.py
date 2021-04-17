from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from marketplace.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price',
                  'created_at', 'updated_at')


# TODO: Rework, add user_id and product_id
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'review_text', 'rating',
                  'created_at', 'updated_at')

    def validate(self, data):
        if self.instance is None:
            if Review.objects.filter(user_id=self.context["request"].user).count() >= 1:
                raise ValidationError
        else:
            pass

        return data


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('Product', 'Order', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    position = OrderProductSerializer(
        source='orederprodust_set',
        read_only=True
    )

    class Meta:
        model = Order
        fields = ('id', 'position', 'status',
                  'created_at', 'updated_at', 'amount')

    def create(self, validated_data):
        position = validated_data.pop('position')

        summary = 0
        for pos in position:
            summary += pos.amount * OrderProduct.Product.price
        instance = Order.objects.create(summary=summary, **validated_data)
        instance.position = position

        return instance


class CompilationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Compilation
        fields = ('heading', 'description', 'product',
                  'created_at', 'updated_at')
