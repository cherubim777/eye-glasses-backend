from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
        #['retailer', 'name', 'image', 'brand', 'category', 'description', 'rating', 'numReviews', 'price', 'countInStock','createdAt' ]