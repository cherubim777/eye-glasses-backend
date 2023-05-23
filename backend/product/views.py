from django.shortcuts import render
from django.http import  JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Product

from .serializers import ProductSerializer
# from .products import product

from django.contrib.auth.models import User
#from .serializers import *
# Create your views here.

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, q): 
    products = Product.objects.filter(
        Q(name__icontains = q) |
        Q(category__icontains = q)
     )
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addProduct(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getRetailerProducts(request,q):
    retailer = User.objects.get(username = q)
    if retailer:
        products = Product.objects.filter(
        Q(retailer__icontains = retailer)
        )
        serializer = ProductSerializer(products, many = False)
        return Response(serializer.data)
    
    else: return Response("no match")
    
@api_view(['POST'])
def deleteProduct(request,q):
    product = Product.objects.get(name = q)
    if request.method == 'POST':
        product.delete()
        return Response("product deleted")
