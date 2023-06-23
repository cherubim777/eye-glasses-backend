from rest_framework import serializers
from .models import *


class CustomerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerNotification
        fields = "__all__"


class RetailerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerNotification
        fields = "__all__"
