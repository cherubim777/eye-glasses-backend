from rest_framework import serializers
from .models import Analytics  # , RetailerAnalytics


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = [
            'retailer',
            'annual_revenue_last_year',
            'annual_revenue_this_year',
            'monthly_revenue',
            'number_of_orders_completed',
            'number_of_products_sold'
        ]
# class RetailerAnal    max_digits=10, decimayticsSerializer(serializers.ModelSerializer):
#     class Meta:   annual_revenue_this_year
#         model = Re    max_digits=10, decimatailerAnalytics
#         fields = [monthly_revenue = models.'__all__']
