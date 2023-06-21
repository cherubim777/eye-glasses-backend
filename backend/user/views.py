from django.shortcuts import get_object_or_404, render
from django.http import Http404, JsonResponse
from django.test import TransactionTestCase
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User, Group


from .serializers import UserSerializer, CustomerSerializer, RetailerSerializer
from django.contrib.auth.hashers import make_password
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
from payment.models import CustomerAccount, RetailerAccount
from payment.serializers import CustomerAccountSerializer, RetailerAccountSerializer
from cart.models import *
from cart.serializers import *
from wishlist.models import *
from wishlist.serializers import *
from rest_framework import generics
from rest_framework import generics, status
import random
from .email import sendMail


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_authenticated and request.user.customer is not None
        except Customer.DoesNotExist:
            return False


class IsRetailer(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_authenticated and request.user.retailer is not None
        except Retailer.DoesNotExist:
            return False


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["email"] = self.user.email
        if hasattr(self.user, "customer"):
            data["userType"] = "customer"
        elif hasattr(self.user, "retailer"):
            data["userType"] = "retailer"
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
    # try:
    with transaction.atomic():
        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password"]),
            email=data["email"],
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
        # Create an account for the new customer with an initial balance of 500
        # this is only to simulate money transaction between customer and retailer
        account = CustomerAccount.create(customer=customer, initial_balance=5000)
        # create cart for the customer

        cart = Cart.create(customer=customer)
        wishlist = WishList.create(customer=customer)
        print("<<<<<<<<<<<<<<<<<or here>>>>>>>>>>>>>>>>>>>>>>>>>")
        user_serializer = UserSerializer(user, many=False)
        customer_serializer = CustomerSerializer(customer, many=False)
        account_serializer = CustomerAccountSerializer(account, many=False)
        cart_serializer = CartSerializer(cart, many=False)
        wishlist_serializer = WishListSerializer(wishlist, many=False)
        response_data = {
            "user": user_serializer.data,
            "customer": customer_serializer.data,
            "account": account_serializer.data,
            "cart": cart_serializer.data,
            "wishlist": wishlist_serializer.data,
        }
        return Response(response_data)
    # except:
    #     message = {"detail": "customer with this username already exists"}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def retailerRegister(request):
    data = request.data
    # try:
    with transaction.atomic():
        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password"]),
            email=data["email"],
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
                custom_order_price=None,
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
                custom_order_price=None,
            )
        # Create an account for the new retailer with an initial balance of 0
        # this is only to simulate maoney transaction
        if "custom_order_price" in data:
            retailer.custom_order_price = data["custom_order_price"]

        account = RetailerAccount.create(retailer=retailer, initial_balance=0)
        user_serializer = UserSerializer(user, many=False)
        retailer_serializer = RetailerSerializer(retailer, many=False)
        account_serializer = RetailerAccountSerializer(account, many=False)
        response_data = {
            "user": user_serializer.data,
            "retailer": retailer_serializer.data,
            "account": account_serializer.data,
        }
        return Response(response_data)
    # except:
    #     message = {"detail": "retailer with this username already exists"}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateCustomer(request):
    customer = request.user.customer
    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateRetailer(request):
    retailer = request.user.retailer

    serializer = RetailerSerializer(retailer, data=request.data, partial=True)

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
@permission_classes([IsAuthenticated])
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


# @api_view(["GET"])
# @permission_classes([IsAuthenticated, IsCustomer])
# def getCustomerProfile(request):
#     user = request.user
#     try:
#         customer = Customer.objects.get(user=user)
#     except Customer.DoesNotExist:
#         return Response(status=404)
#     serializer = CustomerSerializer(customer)
#     return Response(serializer.data)
class GetCustomerProfile(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_object(self):
        user = self.request.user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, customer)
        return customer


class GetCustomerProfileById(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer

    def get_object(self):
        user_id = self.kwargs.get("id")
        if user_id is None:
            user = self.request.user
        else:
            user = get_object_or_404(User, id=user_id)
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, customer)
        return customer


# class GetCustomerProfile(generics.RetrieveAPIView):
#     serializer_class = CustomerSerializer
#     permission_classes = [IsAuthenticated, IsCustomer]

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Customer.objects.filter(user=user)
#         return queryset


# @api_view(["GET"])
# @permission_classes([IsAuthenticated, IsRetailer])
# def getRetailerProfile(request):
#     user = request.user
#     try:
#         retailer = Retailer.objects.get(user=user)
#     except Retailer.DoesNotExist:
#         return Response(status=404)
#     serializer = RetailerSerializer(retailer)
#     return Response(serializer.data)


class GetRetailerProfile(generics.RetrieveAPIView):
    serializer_class = RetailerSerializer
    permission_classes = [IsAuthenticated, IsRetailer]

    def get_object(self):
        user = self.request.user
        try:
            retailer = Retailer.objects.get(user=user)
        except Retailer.DoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, retailer)
        return retailer


# class GetCustomOrderRetailer(generics.RetrieveAPIView):
#     serializer_class = RetailerSerializer
#     # permission_classes = [IsAuthenticated, IsRetailer]

#     def get_object(self):
#         try:
#             queryset = Retailer.objects.filter(accepts_custom_order=True)
#             return queryset

#         except Retailer.DoesNotExist:
#             raise Http404
#         return retailer


class GetCustomOrderRetailer(generics.ListAPIView):
    serializer_class = RetailerSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Retailer.objects.filter(accepts_custom_order=True)
        return queryset


@api_view(["POST"])
def reset_password(request):
    try:
        username = request.data["username"]
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "Username not found"}, status=404)
    else:
        email = user.email
        code = random.randint(10000, 99999)
        if hasattr(user, "customer"):
            user.customer.set_code(code)
        elif hasattr(user, "retailer"):
            user.retailer.set_code(code)

        sendMail(email, code)

        return Response(
            {"message": f"Password reset email sent to {email}"},
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
def confirm_reset(request):
    try:
        username = request.data["username"]
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "Username not found"}, status=404)

    code = request.data["code"]
    password = request.data["password"]
    if hasattr(user, "customer"):
        customer = user.customer
        if customer.reset_password_code == code:
            user.password = make_password(password)
            user.save()
            return Response(
                {"message": "password reset successful"}, status=status.HTTP_200_OK
            )
        else:
            return Response({"message": "Invalid reset password code"}, status=400)

    elif hasattr(user, "retailer"):
        retailer = user.retailer
        if retailer.reset_password_code == code:
            user.password = make_password(password)
            user.save()
            return Response(
                {"message": "password reset successful"}, status=status.HTTP_200_OK
            )
        else:
            return Response({"message": "Invalid reset password code"}, status=400)
