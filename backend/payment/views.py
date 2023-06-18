from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from user.models import *
from payment.models import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCustomerAccount(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
        account = CustomerAccount.objects.get(customer=customer)
    except (Customer.DoesNotExist, CustomerAccount.DoesNotExist):
        account = None
    if account:
        data = {
            "balance": account.balance,
            "reserved_balance": account.reserved_balance,
        }
        return Response(data)
    else:
        return Response({"error": "Account not found"}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getRetailerAccount(request):
    user = request.user
    try:
        retailer = Retailer.objects.get(user=user)
        account = RetailerAccount.objects.get(retailer=retailer)
    except (Retailer.DoesNotExist, RetailerAccount.DoesNotExist):
        account = None
    if account:
        data = {"balance": account.balance}
        return Response(data)
    else:
        return Response({"error": "Account not found"}, status=404)
