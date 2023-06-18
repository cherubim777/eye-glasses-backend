from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from user.models import Customer
from rest_framework.response import Response


class CartView(APIView):
    # authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get_or_create(customer=customer)[0]
        serializer = CartSerializer(cart)
        # another_serializer = CartSerializer(cart.cartitem_set.all())
        return Response(serializer.data)

    def post(self, request):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get_or_create(customer=customer)[0]
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart, product_id=product_id)
            cart_item.quantity = quantity
        cart.refresh_from_db()
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        cart = Cart.objects.get(user=request.user)[0]
        serializer = CartSerializer(cart, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # def delete(self, request):
    #     cart = Cart.objects.get_or_create(user=request.user)[0]
    #     cart.delete()
    #     return Response(status=204)

    def patch(self, request):
        cart = Cart.objects.get(user=request.user)[0]
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        except CartItem.DoesNotExist:
            if quantity > 0:
                serializer.save(cart=cart)
        cart.refresh_from_db()
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data)


class CartItemDeleteView(APIView):
    # def remove_from_cart(self, request, product_id):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        customer = Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        # try:
        #     item = CartItem.objects.filter(cart=cart, product_id=product_id)
        #     if item.quantity > 1:
        #         item.quantity -= 1
        #         item.save()
        #     else:
        #         item.delete()
        # except CartItem.DoesNotExist:
        #     pass
        items = CartItem.objects.filter(cart=cart, product_id=product_id)
        for item in items:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemClearView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer)
        cart.clear_item()
        return Response(status=status.HTTP_204_NO_CONTENT)
