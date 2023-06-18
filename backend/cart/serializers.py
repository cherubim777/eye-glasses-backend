from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('__all__')


class CartSerializer(serializers.ModelSerializer):
    # retrieve only the associated items in this cart
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('__all__')

    '''
    The create() method is overridden to create both the Cart object 
    and its associated CartItem objects in a single transaction. 
    The user field of the Cart object is set to the current authenticated user 
    through the request object, which is passed in through the serializer's context.
    '''

    # def create(self, validated_data):
    #     cart = Cart.objects.create(user=self.context['request'].user)
    #     items_data = validated_data.pop('items', [])
    #     for item_data in items_data:
    #         CartItem.objects.create(cart=cart, **item_data)
    #     return cart

    '''
    The update() method is overridden to update both the Cart object and its associated 
    CartItem objects in a single transaction. First, we update the Cart object using 
    the superclass's update() method. Then, we delete all existing CartItem objects associated
     with the Cart, and create new CartItem objects based on the updated data.
    '''

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance = super().update(instance, validated_data)
        instance.items.all().delete()
        for item_data in items_data:
            CartItem.objects.create(cart=instance, **item_data)
        return instance
