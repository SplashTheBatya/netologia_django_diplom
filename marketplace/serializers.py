from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault

from marketplace.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(default=CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True)
        self.fields['user'] = UserSerializer(read_only=True)
        return super(ReviewSerializer, self).to_representation(instance)

    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        if self.instance is None:
            if Review.objects.filter(user=self.context["request"].user).filter(
                    product=data['product'].id).count() >= 1:
                raise ValidationError('Нельзя')
        else:
            pass

        return data


class OrderProductSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ('Product', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(default=CurrentUserDefault())
    summary = serializers.HiddenField(default=0)
    status = serializers.CharField(default="NEW")
    position = OrderProductSerializer(many=True, source='order_product')

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['summary'] = serializers.IntegerField()
        self.fields['user'] = UserSerializer(read_only=True)
        return super(OrderSerializer, self).to_representation(instance)

    def create(self, validated_data):
        order_product = validated_data.pop("order_product")
        order = Order.objects.create(**validated_data)
        summary = 0
        if "position" in self.initial_data:
            positions = self.initial_data.get("position")
            for pos in positions:
                id = pos.get("Product")
                amount = pos.get("amount")
                product_instance = Product.objects.get(pk=id)
                product_price = product_instance.price
                summary += amount * product_price
                OrderProduct(Order=order, Product=product_instance, amount=amount).save()
        order.summary = summary
        order.save()
        return order


class CompilationSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True, many=True)
        return super(CompilationSerializer, self).to_representation(instance)

    class Meta:
        model = Compilation
        fields = '__all__'
