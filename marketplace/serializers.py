from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from marketplace.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# TODO: Try to return user_id, problem with user serializer
class ReviewSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True)
        return super(ReviewSerializer, self).to_representation(instance)

    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        return super().create(validated_data)

    # TODO: Test validations, may still not be correct
    def validate(self, data):
        print(data)
        if self.instance is None:
            if Review.objects.filter(user_id=self.context["request"].user).filter(product_id=data['product'].id).count()>= 1:
                raise ValidationError
        else:
            pass

        return data


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('Product', 'Order', 'amount')


# TODO: Try use experience from ReviewSerializer
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


# TODO: What can be wrong here...
class CompilationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Compilation
        fields = ('heading', 'description', 'product',
                  'created_at', 'updated_at')
