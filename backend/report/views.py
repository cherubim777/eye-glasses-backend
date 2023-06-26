from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from user.models import *
from payment.models import *
from .models import SalesReport
from .serializers import SalesReportSerializer
from user.views import *


# Create your views here.


class GetSalesReport(generics.RetrieveAPIView):
    serializer_class = SalesReportSerializer
    # permission_classes = [IsAuthenticated, IsRetailer]

    def get_object(self):
        user = self.request.user
        try:
            retailer = Retailer.objects.get(user=user)
            sales_report = SalesReport.objects.get(retailer=retailer)
        except (Retailer.DoesNotExist, SalesReport.DoesNotExist):
            raise Http404
        self.check_object_permissions(self.request, sales_report)
        return sales_report
