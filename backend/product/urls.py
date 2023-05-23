from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('getProducts/', views.getProducts, name="getProducts"),
    path('getProduct/<str:q>/', views.getProduct, name="getProduct"),
    path('addProduct/', views.addProduct, name="addProduct"),
    path('getRetailerProducts/<str:q>/', views.getRetailerProducts, name="getretailerProducts"),
    path('deleteProduct/', views.deleteProduct, name ='deleteProduct')
]