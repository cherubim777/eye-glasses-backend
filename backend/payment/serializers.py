from rest_framework import serializers
from .models import CustomerAccount, RetailerAccount, AdminAccount


class CustomerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAccount
        fields = "__all__"


class RetailerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerAccount
        fields = "__all__"


class AdminAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccount
        fields = "__all__"
