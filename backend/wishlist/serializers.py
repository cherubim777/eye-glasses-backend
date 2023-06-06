from rest_framework import serializers
from .models import WishList, WishListItem


class WishListItemSerializer(serializers.ModelSerializer):
    wishlist = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WishListItem
        fields = ('__all__')


class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        fields = ('__all__')
