from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WishList, WishListItem
from .serializers import WishListSerializer, WishListItemSerializer
from rest_framework.permissions import IsAuthenticated
from user.models import Customer
from product.models import Product


class WishListItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        wishlist = WishList.objects.get(customer=customer)
        items = wishlist.get_items()
        serializer = WishListItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        customer = Customer.objects.get(user=request.user)
        wishlist = WishList.objects.get(customer=customer)
        serializer = WishListItemSerializer(
            data=request.data, context={'wishlist': wishlist})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        customer = Customer.objects.get(user=request.user)
        wishlist = WishList.objects.get(customer=customer)
        product_id = Product.objects.get(id=product_id)
        wishlist.remove_item(product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishListClearView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer = Customer.objects.get(user=request.user)
        wishlist = WishList.objects.get(customer=customer)
        wishlist.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
