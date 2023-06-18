from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
from user.models import Retailer, Customer
from .models import Product, Review
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .serializers import ProductSerializer, ReviewSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from user.views import IsCustomer
from user.views import IsRetailer


class GetProducts(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(quantity__gt=0)
        return queryset


class GetProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"


class FilterProducts(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        q = self.kwargs["q"]
        queryset = Product.objects.filter(
            Q(name__icontains=q)
            | Q(gender_category__icontains=q)
            | Q(age_group__icontains=q)
            | Q(category__icontains=q)
        )
        return queryset


class AddProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            try:
                retailer = Retailer.objects.get(user=request.user)
            except Retailer.DoesNotExist:
                return Response(
                    {"error": "Only retailers can add products"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer.save(retailer=retailer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRetailerProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        retailer = Retailer.objects.get(user=self.request.user)
        queryset = Product.objects.filter(retailer=retailer)
        return queryset


class DeleteProduct(APIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsRetailer]

    def get_queryset(self):
        return Product.objects.filter(retailer=self.request.user.retailer)

    def delete(self, request, pk):
        try:
            instance = self.get_queryset().get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.delete()
        return Response(
            {"success": "Product deleted successfully"},
            status=status.HTTP_200_OK,
            content_type="application/json",
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
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not request.user.is_authenticated or not hasattr(request.user, "retailer"):
            return Response(
                {"error": "Authentication failed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if product.retailer.user_id != request.user.id:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addReview(request, pk):
    customer = request.user.customer

    product = get_object_or_404(Product, id=pk)
    rating = request.data.get("rating")
    review = Review(
        product=product,
        customer=customer,
        retailer=product.retailer,
        rating=request.data.get("rating"),
        comment=request.data.get("comment"),
    )

    review.save()
    product.calculateRating(rating)

    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(["GET"])
def getReviews(request, pk):
    product = get_object_or_404(Product, id=pk)

    reviews = Review.objects.filter(product=product)

    serializer = ReviewSerializer(reviews, many=True)

    return Response(serializer.data)
