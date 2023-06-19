from rest_framework import serializers
from .models import WishList, WishListItem
from product.serializers import ProductSerializer
from product.models import Product


class WishListItemSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = WishListItem
        fields = ['id', 'wishlist', 'product_id', 'added_date', 'purchased']

    def create(self, validated_data):
        wishlist = self.context['wishlist']
        product_id = validated_data['product_id']
        return wishlist.add_item(product_id)


class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        fields = ['id', 'customer', 'date_created', 'items']

    def create(self, validated_data):
        customer = self.context['request'].user.customer
        validated_data['customer'] = customer
        return super().create(validated_data)
