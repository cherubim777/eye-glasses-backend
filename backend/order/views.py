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
    shipping_price = Decimal("5.00")  # assuming flat shipping rate of 5.00 birr
    total_price = item_price + shipping_price

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
        postalCode=shipping_address.get("postalCode"),
        country=shipping_address.get("country"),
        shippingPrice=shipping_price,
    )

    # Serialize the order and return it in the response
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getRetailerOrder(request, pk):
    # Retrieve the authenticated user
    user = request.user

    # Get the retailer associated with the provided retailer_id
    try:
        retailer = Retailer.objects.get(id=pk)
    except Retailer.DoesNotExist:
        return Response(
            {"error": f"Retailer with id {pk} does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check that the authenticated user is associated with the retailer
    if user.retailer != retailer:
        return Response(
            {"error": "You are not authorized to view orders for this retailer"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Get all orders associated with the retailer
    orders = Order.objects.filter(retailer=retailer)

    # Serialize the orders and return them in the response
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsCustomer, IsAdminUser])
def placeCartOrder(request):
    cart = get_object_or_404(Cart, user=request.user)

    # Group cart items by retailer
    cart_items_by_retailer = {}
    for cart_item in cart.items.all():
        retailer = cart_item.product.retailer
        if retailer not in cart_items_by_retailer:
            cart_items_by_retailer[retailer] = []
        cart_items_by_retailer[retailer].append(cart_item)

    # Create an order for each retailer and calculate the total price for each order
    orders = []
    for retailer, cart_items in cart_items_by_retailer.items():
        # Create a new order
        order = Order.objects.create(
            customer=request.user.customer,
            retailer=retailer,
            paymentMethod=request.POST.get("paymentMethod"),
            shippingPrice=None,
            totalPrice=None,
        )

        # Add order items to the order and calculate the total price for the order
        total_price = Decimal("0.00")
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                product=cart_item.product,
                order=order,
                name=cart_item.product.name,
                qty=cart_item.quantity,
                price=cart_item.product.price,
            )
            total_price += cart_item.product.price * cart_item.quantity

        # Calculate the total price including tax and shipping for the order

        shipping_price = Decimal("0.00")  # TODO: calculate shipping price for the order
        commission_price = Decimal("0.00")
        commission_rate = Decimal("0.02")  # 2% commission rate
        commission_price = total_price * commission_rate
        total_price += shipping_price + commission_price

        # Update the order with the total price, tax price, shipping price, and commission price

        order.shippingPrice = shipping_price
        order.commissionPrice = commission_price
        order.totalPrice = total_price
        order.save()

        # Create a new shipping address for the order
        shipping_address = ShippingAddress.objects.create(
            order=order,
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            postalCode=request.POST.get("postalCode"),
            country=request.POST.get("country"),
            shippingPrice=shipping_price,
        )

        # Add the order to the list of orders
        orders.append(order)

    # Clear the items in the cart
    cart.items.clear()

    # Serialize the list of orders
    serializer = OrderSerializer(orders, many=True)

    # Return a response with the serialized data
    return Response(serializer.data)


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
