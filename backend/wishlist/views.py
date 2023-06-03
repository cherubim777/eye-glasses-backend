# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from .models import WishList, WishListItem
# from .serializers import WishListSerializer, WishListItemSerializer


# class WishListView(APIView):
#     def get(self, request):
#         WishLists = WishList.objects.all()
#         serializer = WishListSerializer(WishLists, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = WishListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class WishListDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return WishList.objects.get(pk=pk)
#         except WishList.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         WishList = self.get_object(pk)
#         serializer = WishListSerializer(WishList)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         WishList = self.get_object(pk)
#         serializer = WishListSerializer(WishList, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         WishList = self.get_object(pk)


# class WishListDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return WishList.objects.get(pk=pk)
#         except WishList.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         WishList = self.get_object(pk)
#         serializer = WishListSerializer(WishList)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         WishList = self.get_object(pk)
#         serializer = WishListSerializer(WishList, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         WishList = self.get_object(pk)
#         WishList.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import WishList, WishListItem
from product.models import Product
from .serializers import WishListSerializer, WishListItemSerializer


class WishListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        serializer = WishListSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishListItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            # product = Product.objects.get(id=product_id)
            wishlist, created = WishList.objects.get_or_create(
                user=request.user)
            item = WishListItem.objects.create(
                wishlist=wishlist, product=product)
            serializer = WishListSerializer(wishlist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        try:
            item = WishListItem.objects.get(
                product=item_id, wishlist=WishList.objects.get(user=request.user))
        except WishListItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
