from django.shortcuts import render
from django.http import JsonResponse
from django.test import TransactionTestCase
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User, Group


from .serializers import UserSerializer, CustomerSerializer, RetailerSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import *
from .serializers import *
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_authenticated and request.user.customer is not None
        except Customer.DoesNotExist:
            return False


class IsRetailer(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_authenticated and request.user.customer is not None
        except Retailer.DoesNotExist:
            return False


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["email"] = self.user.email
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class Logout(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = []

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        access_token = request.data.get("access_token")

        logout(request)

        if refresh_token:
            try:
                TokenRefreshView().blacklist(refresh_token)
            except TokenError as e:
                return Response({"detail": str(e)}, status=400)

        if access_token:
            try:
                TokenObtainPairView().blacklist(access_token)
            except TokenError as e:
                return Response({"detail": str(e)}, status=400)

        return Response({"message": "User logged out successfully"})


@api_view(["POST"])
def customerRegister(request):
    data = request.data
    try:
        with transaction.atomic():
            
            user = User.objects.create(
                username=data["username"],
                password=make_password(data["password"]),
            )
            if "photo" in data:
                customer = Customer.objects.create(
                    user=user,
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    phone_number=data["phone_number"],
                    email=data["email"],
                    local_address=data["local_address"],
                    subcity=data["subcity"],
                    city=data["city"],
                    photo=data["photo"],
                )
            else:
                customer = Customer.objects.create(
                    user=user,
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    phone_number=data["phone_number"],
                    email=data["email"],
                    local_address=data["local_address"],
                    subcity=data["subcity"],
                    city=data["city"],
                )
            
            user_serializer = UserSerializer(user, many=False)
            customer_serializer = CustomerSerializer(customer, many=False)
            response_data = {
                "user": user_serializer.data,
                "customer": customer_serializer.data,
            }
            return Response(response_data)
    except:
        message = {"detail": "customer with this username already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def retailerRegister(request):
    data = request.data
    try:
        with transaction.atomic():
            
            user = User.objects.create(
                username=data["username"],
                password=make_password(data["password"]),
            )
            if "photo" in data:
                retailer = Retailer.objects.create(
                    user=user,
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    phone_number=data["phone_number"],
                    email=data["email"],
                    local_address=data["local_address"],
                    subcity=data["subcity"],
                    city=data["city"],
                    photo=data["photo"],
                    store_name=data["store_name"],
                    accepts_custom_order=data["accepts_custom_order"],
                )
            else:
                retailer = Retailer.objects.create(
                    user=user,
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    phone_number=data["phone_number"],
                    email=data["email"],
                    local_address=data["local_address"],
                    store_name=data["store_name"],
                    subcity=data["subcity"],
                    city=data["city"],
                    accepts_custom_order=data["accepts_custom_order"],
                )
            
            user_serializer = UserSerializer(user, many=False)
            retailer_serializer = RetailerSerializer(retailer, many=False)
            response_data = {
                "user": user_serializer.data,
                "retailer": retailer_serializer.data,
            }
            return Response(response_data)
    except:
        message = {"detail": "retailer with this username already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateCustomer(request):
    customer = request.user.customer
    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateRetailer(request):
    retailer = request.user.retailer
    serializer = RetailerSerializer(retailer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getAllCustomers(request):
    customers = Customer.objects.select_related("user").all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getAllRetailers(request):
    retailers = Retailer.objects.select_related("user").all()
    serializer = RetailerSerializer(retailers, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateUser(request):
    user = request.user
    data = request.data
    if "username" in data:
        user.username = data["username"]
    if "password" in data:
        user.password = make_password(data["password"])
    user.save()
    return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def deleteAccount(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getCustomerProfile(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return Response(status=404)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getRetailerProfile(request):
    user = request.user
    try:
        retailer = Retailer.objects.get(user=user)
    except Retailer.DoesNotExist:
        return Response(status=404)
    serializer = RetailerSerializer(retailer)
    return Response(serializer.data)
