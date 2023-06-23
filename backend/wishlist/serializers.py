from rest_framework import serializers
from .models import WishList, WishListItem
from product.serializers import ProductSerializer
from product.models import Product


class WishListItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)['id']
    # product_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = WishListItem
        # fields = ['id', 'wishlist', 'product_id', 'added_date', 'purchased']
        fields = ['id', 'wishlist', 'product',
                  'product_id', 'added_date', 'purchased']

    def create(self, validated_data):
        wishlist = self.context['wishlist']
        product = validated_data['product'].id
        return wishlist.add_item(product)


class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerializer(many=True, read_only=True)
    product_items = serializers.ListField(child=serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()), write_only=True, required=False)

    class Meta:
        model = WishList
        fields = ['id', 'customer', 'date_created', 'items', 'product_items']

    def create(self, validated_data):
        customer = self.context['request'].user.customer
        validated_data['customer'] = customer

        # add product items to the wishlist
        product_items = validated_data.get('product_items', [])
        for product_id in product_items:
            wishlist.add_item(product_id)
        return super().create(validated_data)
