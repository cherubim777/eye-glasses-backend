from datetime import timezone
import datetime
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
from payment.models import CustomerAccount, RetailerAccount, AdminAccount
from product.serializers import *
from rest_framework.views import APIView
from notification.models import *


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCustomer])
def placeOrder(request):
    # Retrieve the necessary data from the request
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity")
    shipping_address = request.data.get("shipping_address")
    payment_method = request.data.get("payment_method")
    delivery = request.data.get("delivery")
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
        account = user.customer.customeraccount
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

    # Check if the product has enough quantity to fulfill the order
    if product.quantity < int(quantity):
        return Response(
            {"error": "Insufficient product quantity"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Decrease the product quantity by the ordered amount
    if not product.decrease_quantity(amount=quantity):
        # The product quantity is less than the ordered amount
        return Response(
            {"error": "Insufficient product quantity"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Calculate the total price of the order
    item_price = product.price
    shipping_price = Decimal("100.00")
    # assuming flat shipping rate of 100.00 birr
    commission_rate = 0.02 * float(item_price)
    total_price = (
        item_price * Decimal(quantity) + shipping_price + Decimal(commission_rate)
    )

    # Check if the customer has enough balance to place the order
    if account.balance < total_price:
        return Response(
            {"error": "Insufficient balance"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Decrease the customer's balance and increase the reserved balance
    account.decrease_balance(total_price)
    account.reserved_balance += total_price

    # Create a new order
    order = Order.objects.create(
        customer=customer,
        retailer=retailer,
        paymentMethod=payment_method,
        shippingPrice=shipping_price,
        totalPrice=total_price,
        commissionPrice=commission_rate,
        delivery=delivery,
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
    shipping_address = request.data.get("shipping_address")
    frame = request.data.get("frame")
    retailer_id = request.data.get("retailer")
    right_sphere = request.data.get("right_sphere")
    left_sphere = request.data.get("left_sphere")
    right_cylinder = request.data.get("right_cylinder")
    left_cylinder = request.data.get("left_cylinder")
    right_axis = request.data.get("right_axis")
    left_axis = request.data.get("left_axis")
    right_prism = request.data.get("right_prism")
    left_prism = request.data.get("left_prism")
    payment_method = request.data.get("payment_method")
    delivery = request.data.get("delivery")
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
    account = customer.customeraccount

    # Get the retailer for the custom order
    try:
        retailer = Retailer.objects.get(user=retailer_id)
    except Retailer.DoesNotExist:
        return Response(
            {"error": f"Retailer with id {retailer_id} does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        frame = Product.object.get(id=frame)
    except frame.DoesNotExist:
        return Response(
            {"error": "This frame doesnot exist any more"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if retailer.accepts_custom_order != True:
            raise ValueError(
                f"Retailer with id {retailer_id} does not accept custom orders"
            )

    except ValueError as e:
        return Response({"error": str(e)})

    # Calculate the total price of the custom order
    item_price = (
        retailer.custom_order_price + frame.price
    )  # assuming price per custom order is 500.00 birr
    shipping_price = Decimal("100.00")  # assuming flat shipping rate of 100.00 birr
    commission_rate = Decimal("0.02")  # assuming commission rate of 2%
    commission_price = item_price * commission_rate
    total_price = item_price + shipping_price + commission_price

    # Check if the customer has enough balance to place the order
    if account.balance < total_price:
        return Response(
            {"error": "Insufficient balance"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Decrease the customer's balance and increase the reserved balance
    account.decrease_balance(total_price)
    account.reserved_balance += total_price

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
        delivery=delivery,
        frame=frame,
    )

    # Create a new shipping address
    ShippingAddress.objects.create(
        order=custom_order,
        address=shipping_address.get("address"),
        city=shipping_address.get("city"),
        shippingPrice=shipping_price,
    )

    # Serialize the custom order and return it in the response
    serializer = CustomOrderSerializer(custom_order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsRetailer])
def getRetailerCustomOrders(request):
    # Retrieve the authenticated user
    user = request.user

    # Get the retailer associated with the user
    try:
        retailer = user.retailer
    except retailer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a retailer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    order_dict = []
    # Retrieve the retailer's custom orders
    custom_orders = CustomOrder.objects.filter(retailer=retailer).order_by("-createdAt")
    for order in custom_orders:
        customer_first_name = order.customer.first_name
        customer_last_name = order.customer.last_name
        customer = f"{customer_first_name} {customer_last_name}"
        retailer_first_name = order.retailer.first_name
        retailer_last_name = order.retailer.last_name
        retailer = f"{retailer_first_name} {retailer_last_name}"
        store_name = order.retailer.store_name

        order_data = {
            "customer": customer,
            "retailer": retailer,
            "store_name": store_name,
        }
        # Serialize the custom orders and return them in the response
        data_serializer = OrderDataSerializer(data=order_data)
        serializer = CustomOrderSerializer(order, many=False)
        if serializer.is_valid:
            the_order = {
                "custom_order": serializer.data,
                "order_data": data_serializer.initial_data,
            }
            order_dict.append(the_order)
        else:
            errors = serializer.errors

    return Response({"custom_orders": order_dict})


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCustomer])
def getCustomerCustomOrders(request):
    # Retrieve the authenticated user
    user = request.user

    # Get the retailer associated with the user
    try:
        customer = user.customer
    except customer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a customer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    order_dict = []
    # Retrieve the retailer's custom orders
    custom_orders = CustomOrder.objects.filter(customer=customer).order_by("-createdAt")
    for order in custom_orders:
        customer_first_name = order.customer.first_name
        customer_last_name = order.customer.last_name
        customer = f"{customer_first_name} {customer_last_name}"
        retailer_first_name = order.retailer.first_name
        retailer_last_name = order.retailer.last_name
        retailer = f"{retailer_first_name} {retailer_last_name}"
        store_name = order.retailer.store_name

        order_data = {
            "customer": customer,
            "retailer": retailer,
            "store_name": store_name,
        }
        # Serialize the custom orders and return them in the response
        data_serializer = OrderDataSerializer(data=order_data)
        serializer = CustomOrderSerializer(order, many=False)
        if serializer.is_valid:
            the_order = {
                "custom_order": serializer.data,
                "order_data": data_serializer.initial_data,
            }
            order_dict.append(the_order)
        else:
            errors = serializer.errors

    return Response({"custom_orders": order_dict})


class GetRetailerOrders(APIView):
    permission_classes = [IsAuthenticated, IsRetailer]

    def get(self, request, format=None):
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
        order_dict = []
        orders = Order.objects.filter(retailer=retailer).order_by("-createdAt")
        for order in orders:
            order_serializer = OrderSerializer(order, many=False)
            customer_first_name = order.customer.first_name
            customer_last_name = order.customer.last_name
            customer = f"{customer_first_name} {customer_last_name}"
            retailer_first_name = order.retailer.first_name
            retailer_last_name = order.retailer.last_name
            retailer = f"{retailer_first_name} {retailer_last_name}"
            store_name = order.retailer.store_name
            order_item = OrderItem.objects.get(order=order)
            quantity = order_item.qty
            product = order_item.product
            image = request.build_absolute_uri(product.photo.url)
            product_name = product.name

            order_data = {
                "customer": customer,
                "retailer": retailer,
                "store_name": store_name,
                "quantity": quantity,
                "photo": image,
                "product_name": product_name,
            }
            serializer = OrderDataSerializer(data=order_data)
            if serializer.is_valid:
                the_order = {
                    "order": order_serializer.data,
                    "order_data": serializer.initial_data,
                }
                order_dict.append(the_order)
            else:
                errors = serializer.errors

        return Response({"orders": order_dict})


class GetCustomerOrders(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, format=None):
        # Retrieve the authenticated user
        user = request.user

        # Get the retailer associated with the user
        try:
            customer = user.customer
        except customer.DoesNotExist:
            return Response(
                {"error": "This user is not associated with a retailer account"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrieve the retailer's orders (that are not custom orders)
        order_dict = []
        orders = Order.objects.filter(customer=customer).order_by("-createdAt")
        for order in orders:
            order_serializer = OrderSerializer(order, many=False)
            customer_first_name = order.customer.first_name
            customer_last_name = order.customer.last_name
            customer = f"{customer_first_name} {customer_last_name}"
            retailer_first_name = order.retailer.first_name
            retailer_last_name = order.retailer.last_name
            retailer = f"{retailer_first_name} {retailer_last_name}"
            store_name = order.retailer.store_name
            order_item = OrderItem.objects.get(order=order)
            quantity = order_item.qty
            product = order_item.product
            image = request.build_absolute_uri(product.photo.url)
            product_name = product.name

            order_data = {
                "customer": customer,
                "retailer": retailer,
                "store_name": store_name,
                "quantity": quantity,
                "photo": image,
                "product_name": product_name,
            }
            serializer = OrderDataSerializer(data=order_data)
            if serializer.is_valid:
                the_order = {
                    "order": order_serializer.data,
                    "order_data": serializer.initial_data,
                }
                order_dict.append(the_order)
            else:
                errors = serializer.errors

        return Response({"orders": order_dict})


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
    custom_order.readyAt = datetime.datetime.now()
    custom_order.save()

    CustomerNotification.objects.create(
        customer=custom_order.customer,
        message=f" the custom order you have ordered from {retailer} at {custom_order.createdAt} is ready",
    )

    # Serialize the custom order and return it in the response
    serializer = CustomOrderSerializer(custom_order)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsCustomer])
def orderFulfilled(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
        )
    if not order.isDelivered:
        order_item = OrderItem.objects.get(order=order)
        retailer_account = order.retailer.retaileraccount
        customer_account = order.customer.customeraccount
        customer_account.fulfill_order(order.totalPrice, retailer_account)
        order.isDelivered = True
        order.deliveredAt = datetime.datetime.now()
        order.save()

        RetailerNotification.objects.create(
            retailer=order.retailer,
            message=f" the product {order_item.product.name} has been succesuly delivered to {order.customer.name} therefore the money is delivered to your account",
        )

    return Response({"message": "money transferred to retailer account"})


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsCustomer])
def CustomOrderFulfilled(request, order_id):
    order = CustomOrder.objects.get(id=order_id)
    if order.isReady:
        if not order.isDelivered:
            retailer_account = order.retailer.retaileraccount
            customer_account = order.customer.customeraccount
            customer_account.fulfill_order(order.totalPrice, retailer_account)
            order.isDelivered = True
            order.deliveredAt = datetime.datetime.now()
            order.save()
            RetailerNotification.objects.create(
                retailer=order.retailer,
                message=f" the custom order has been succesuly delivered to {order.customer.name} therefore the money is delivered to your account",
            )

        return Response({"message": "money transferred to retailer account"})
    else:
        return Response({"message": "order is not ready yet"})


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCustomer])
def placeCartOrder(request):
    # Retrieve the necessary data from the request
    shipping_address = request.data.get("shipping_address")
    payment_method = request.data.get("payment_method")
    delivery = request.data.get("delivery")

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
        account = user.customer.customeraccount
    except Customer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a customer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get the customer's cart
    try:
        cart = customer.cart
    except Cart.DoesNotExist:
        return Response(
            {"error": "This customer does not have a cart"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Calculate the shipping price and commission rate
    shipping_price = Decimal("100.00")
    commission_rate = Decimal("0.02")

    # Iterate through each item in the cart and create a new order for each item
    orders = []
    for cart_item in cart.items.all():
        # Get the product associated with the cart item
        product = cart_item.product_id
        retailer = product.retailer

        # Check if the product has enough quantity to fulfill the order
        if product.quantity < cart_item.quantity:
            return Response(
                {"error": f"Insufficient product quantity for {product.name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Decrease the product quantity by the ordered amount
        if not product.decrease_quantity(amount=cart_item.quantity):
            # The product quantity is less than the ordered amount
            return Response(
                {"error": f"Insufficient product quantity for {product.name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate the total price for the order item
        item_price = product.price
        commission_amount = commission_rate * item_price * Decimal(cart_item.quantity)
        total_price = (
            item_price * Decimal(cart_item.quantity)
            + shipping_price
            + commission_amount
        )

        # Check if the customer has enough balance to place the order
        if account.balance < total_price:
            return Response(
                {"error": "Insufficient balance"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Decrease the customer's balance and increase the reserved balance
        account.decrease_balance(total_price)
        account.reserved_balance += total_price

        # Create a new order
        order = Order.objects.create(
            customer=customer,
            retailer=retailer,
            paymentMethod=payment_method,
            shippingPrice=shipping_price,
            totalPrice=total_price,
            commissionPrice=commission_amount,
            delivery=delivery,
        )

        # Create a new order item
        OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            qty=cart_item.quantity,
            price=item_price,
        )

        # Create a new shipping address
        ShippingAddress.objects.create(
            order=order,
            address=shipping_address.get("address"),
            city=shipping_address.get("city"),
            shippingPrice=shipping_price,
        )

        # Add the order to the list of orders
        orders.append(order)

    # Clear the customer's cart
    # cart.items.delete()

    # Serialize the orders and return them in the response
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetNumberOfOrders(APIView):
    permission_classes = [IsAuthenticated, IsRetailer]

    def get(self, request, format=None):
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

        orders = Order.objects.filter(retailer=retailer)
        custom_orders = CustomOrder.objects.filter(retailer=retailer)
        order_count = orders.count() + custom_orders.count()

        return Response({"order_count": order_count})


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsRetailer])
def getNumberOfCustomOrders(request):
    # Retrieve the authenticated user
    user = request.user

    # Get the retailer associated with the user
    try:
        retailer = user.retailer
    except retailer.DoesNotExist:
        return Response(
            {"error": "This user is not associated with a retailer account"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Retrieve the retailer's custom orders
    custom_orders = CustomOrder.objects.filter(retailer=retailer)
    custom_order_count = custom_orders.count()
    return Response({"order_count": custom_order_count})
