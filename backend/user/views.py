from django.shortcuts import render
from django.http import  JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
# from .products import product
#from .models import Product
#from .serializers import *

# api_view(['POST'])
# def createCustomer(request):
#     user = 


api_view(['POST'])
def CustomerRegister(request):
    data = request.data
    registeringCustomer = User.objects.create(
        user = data['body']
            )
    return Response("user created")