from django.contrib import admin
from .models import Analytics  # , RetailerAnalytics

# Register your models here.
admin.site.register(Analytics)
# admin.site.register(RetailerAnalytics)


# class AnalyticsAdmin(admin.ModelAdmin):
#     readonly_fields = ('anual_revenue_last_year', 'anual_revenue_this_year',
#                        'monthly_revenue', 'number_of_orders_completed', 'retailer', 'analytics')

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         del actions['delete_selected']
#         return actions

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False


# admin.site.register(Analytics, AnalyticsAdmin)
# admin.site.register(RetailerAnalytics, AnalyticsAdmin)
