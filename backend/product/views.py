from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from user.models import Customer
from .models import Product, Review
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .serializers import ProductSerializer, ReviewSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from user.views import IsCustomer


@api_view(["GET"])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def filterProducts(request, q):
    products = Product.objects.filter(
        Q(name__icontains=q)
        | Q(gender_category__icontains=q)
        | Q(age_group__icontains=q)
    )
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


class AddProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, "retailer"):
            return Response(
                {"error": "Only retailers can add products"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(retailer=request.user.retailer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRetailerProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        return Product.objects.filter(retailer=self.request.user.retailer)


class DeleteProduct(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        return Product.objects.filter(retailer=self.request.user.retailer)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(
            {"success": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class RelatedProduct(APIView):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)

        related_products = Product.objects.filter(
            Q(category=product.gender_category) & ~Q(pk=product.pk)
        )

        serializer = ProductSerializer(related_products, many=True)
        return Response(serializer.data)


class UpdateProduct(APIView):
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.retailer != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsCustomer])
def addReview(request, pk):
    product = Product.objects.get(pk=pk)

    review_data = {
        "product": product.id,
        "user": request.user.id,
        "rating": request.data.get("rating", None),
        "comment": request.data.get("comment", None),
    }
    serializer = ReviewSerializer(data=review_data)
    if serializer.is_valid():
        serializer.save()
        product.num_reviews += 1
        product.save()
        response_data = {
            "product": ProductSerializer(product).data,
            "review": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviews(APIView):
    def get(self, request, pk):
        reviews = Review.objects.filter(product=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
