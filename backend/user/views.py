from django.shortcuts import render
from django.http import  JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User, Group 
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
       data =  super().validate(attrs) 
       data['username'] = self.user.username
       data['email'] = self.user.email
       return data
    
       
       
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def customerRegister(request):
    
    group = Group.objects.get(name='customer')
    data = request.data
    try:
        user = User.objects.create(
        username = data['username'],
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        password = make_password(data['password']),
         )
        user.groups.add(group)
        serializer = UserSerializer(user, many = False)
        return Response(serializer.data)
    except:  
        message = {'detail' : 'customer with this username already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def retailerRegister(request):
    group = Group.objects.get(name='retailer')
    data = request.data
    try:
        user = User.objects.create(
        username = data['username'],
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        password = make_password(data['password']),
         )
        user.groups.add(group)
        serializer = UserSerializer(user, many = False)
        return Response(serializer.data)
    except:
        message = {'detail' : 'retailer with this username already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PUT'])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many = False)
    data = request.data
    
    