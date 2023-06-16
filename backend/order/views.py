from datetime import timezone
from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view

# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from user.models import *
from product.models import *
from user.views import IsCustomer, IsRetailer
from cart.models import Cart


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCustomer])
def placeOrder(request):
    # Retrieve the necessary data from the request
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity")
    shipping_address = request.data.get("shipping_address")
    payment_method = request.data.get("payment_method")

    # Retrieve the authenticated user
    user = request.user

    # Get the customer associated with the user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a customer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        account = user.customer.account
    except Customer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a customer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get the retailer associated with the product
    try:
        product = Product.objects.get(id=product_id)
        retailer = product.retailer
    except Product.DoesNotExist:
        return Response(
            {"error": f"Product with id {product_id} does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Calculate the total price of the order
    item_price = product.price
    shipping_price = Decimal("100.00")  # assuming flat shipping rate of 5.00 birr
    total_price = item_price * Decimal(quantity) + shipping_price

    # Check if the customer has enough balance to place the order
    if account.balance < total_price:
        return Response(
            {"error": "Insufficient balance"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Decrease the customer's balance and increase the reserved balance
    account.decrease_balance(total_price)

    # Create a new order
    order = Order.objects.create(
        customer=customer,
        retailer=retailer,
        paymentMethod=payment_method,
        shippingPrice=shipping_price,
        totalPrice=total_price,
    )

    # Create a new order item
    OrderItem.objects.create(
        product=product,
        order=order,
        name=product.name,
        qty=quantity,
        price=item_price,
    )

    # Create a new shipping address
    ShippingAddress.objects.create(
        order=order,
        address=shipping_address.get("address"),
        city=shipping_address.get("city"),
        shippingPrice=shipping_price,
    )

    # Serialize the order and return it in the response
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCustomer])
def placeCustomOrder(request):
    # Retrieve the necessary data from the request
    retailer_id = request.data.get("retailer_id")
    right_sphere = request.data.get("right_sphere")
    left_sphere = request.data.get("left_sphere")
    right_cylinder = request.data.get("right_cylinder")
    left_cylinder = request.data.get("left_cylinder")
    right_axis = request.data.get("right_axis")
    left_axis = request.data.get("left_axis")
    right_prism = request.data.get("right_prism")
    left_prism = request.data.get("left_prism")
    payment_method = request.data.get("payment_method")

    # Retrieve the authenticated user
    user = request.user

    # Get the customer associated with the user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a customer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get the retailer for the custom order
    try:
        retailer = Retailer.objects.get(id=retailer_id)
    except Retailer.DoesNotExist:
        return Response(
            {"error": f"Retailer with id {retailer_id} does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Calculate the total price of the custom order
    item_price = Decimal("50.00")  # assuming price per custom order is 50.00 birr
    shipping_price = Decimal("10.00")  # assuming flat shipping rate of 10.00 birr
    commission_rate = Decimal("0.02")  # assuming commission rate of 2%
    commission_price = item_price * commission_rate
    total_price = item_price + shipping_price + commission_price

    # Create a new custom order
    custom_order = CustomOrder.objects.create(
        customer=customer,
        retailer=retailer,
        rightSphere=right_sphere,
        leftSphere=left_sphere,
        rightCylinder=right_cylinder,
        leftCylinder=left_cylinder,
        rightAxis=right_axis,
        leftAxis=left_axis,
        rightPrism=right_prism,
        leftPrism=left_prism,
        paymentMethod=payment_method,
        shippingPrice=shipping_price,
        commissionPrice=commission_price,
        totalPrice=total_price,
    )

    # Serialize the custom order and return it in the response
    serializer = CustomOrderSerializer(custom_order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def getCustomerCustomOrders(request):
    # Retrieve the authenticated user
    user = request.user

    # Get the customer associated with the user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a customer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Retrieve the customer's custom orders
    custom_orders = CustomOrder.objects.filter(customer=customer).order_by("-createdAt")

    # Serialize the custom orders and return them in the response
    serializer = CustomOrderSerializer(custom_orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsRetailer])
def getRetailerCustomOrders(request):
    # Retrieve the authenticated user
    user = request.user

    # Get the retailer associated with the user
    try:
        retailer = user.retailer
    except Retailer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a retailer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Retrieve the retailer's custom orders
    custom_orders = CustomOrder.objects.filter(retailer=retailer).order_by("-createdAt")

    # Serialize the custom orders and return them in the response
    serializer = CustomOrderSerializer(custom_orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsRetailer])
def getRetailerNotCustomrOrders(request):
    # Retrieve the authenticated user
    user = request.user

    # Get the retailer associated with the user
    try:
        retailer = user.retailer
    except Retailer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a retailer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Retrieve the retailer's orders (that are not custom orders)
    orders = Order.objects.filter(retailer=retailer, customOrder=None).order_by(
        "-createdAt"
    )

    # Serialize the orders and return them in the response
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def getCustomerNotCustomOrders(request):
    # Retrieve the authenticated user
    user = request.user

    # Get the customer associated with the user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a customer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Retrieve the customer's orders (that are not custom orders)
    orders = Order.objects.filter(customer=customer, customOrder=None).order_by(
        "-createdAt"
    )

    # Serialize the orders and return them in the response
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsRetailer])
def markCustomOrderAsReady(request, custom_order_id):
    # Retrieve the authenticated user
    user = request.user

    # Get the retailer associated with the user
    try:
        retailer = user.retailer
    except Retailer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a retailer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Retrieve the custom order to be marked as ready
    try:
        custom_order = CustomOrder.objects.get(id=custom_order_id, retailer=retailer)
    except CustomOrder.DoesNotExist:
        return Response(
            {
                "error": f"Custom order with id {custom_order_id} does not exist or does not belong to this retailer"
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Update the custom order fields
    custom_order.isReady = True
    custom_order.readyAt = timezone.now()
    custom_order.save()

    # Serialize the custom order and return it in the response
    serializer = CustomOrderSerializer(custom_order)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsCustomer])
def updateIsDelivered(request, order_id):
    try:
        # Retrieve the order instance by ID and check if it belongs to the authenticated user
        order = Order.objects.get(id=order_id, customer=request.user.customer)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Set the is_delivered flag to True and save the order instance
    order.is_delivered = True
    order.save()

    # Return a success response
    return Response(status=status.HTTP_200_OK)
