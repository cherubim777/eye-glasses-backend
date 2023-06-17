from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress, CustomOrder


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class ShippingAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAdressSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class CustomOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrder
        fields = "__all__"
