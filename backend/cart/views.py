# from rest_framework import permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Cart, CartItem
# from .serializers import CartSerializer, CartItemSerializer
#
#
# class CartListView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, format=None):
#         carts = Cart.objects.all()
#         serializer = CartSerializer(carts, many=True)
#         return Response(serializer.data)
#
#
# class CartDetailView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, format=None, user_name=None):
#         cart = Cart.objects.get(customer=request.user)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
#
#     def post(self, request, format=None, user_name=None):
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(customer=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, format=None, user_name=None):
#         cart = Cart.objects.get(customer=request.user)
#         serializer = CartSerializer(cart, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, format=None, user_name=None):
#         cart = Cart.objects.get(customer=request.user)
#         cart.delete()
#         return Response(status=204)
#

from rest_framework import generics, permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


# CartListCreateAPIView: handles HTTP GET and POST requests
#  for listing all carts and creating new carts, respectively.

class CartListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print(self.request.user, '------------')
        serializer.save(user=self.request.user)


'''
    CartRetrieveUpdateDestroyAPIView: handles HTTP GET, PUT, and DELETE requests 
    for retrieving, updating, and deleting a specific cart, respectively.
'''


class CartRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


'''
    CartItemCreateAPIView: handles HTTP POST requests for adding a new item to the cart.
'''


class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)


'''
    CartItemRetrieveUpdateDestroyAPIView: handles HTTP GET, PUT, and DELETE requests 
    for retrieving, updating, and deleting a specific item in the cart, respectively.
'''


class CartItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
