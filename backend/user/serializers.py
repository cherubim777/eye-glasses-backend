from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        extra_kwargs = {
            "photo": {"required": False},  # Make photo field optional
        }


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = "__all__"
