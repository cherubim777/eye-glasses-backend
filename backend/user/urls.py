from django.contrib import admin
from django.urls import path, include
from . import views




urlpatterns = [
   path('login/', views.MyTokenObtainPairView.as_view(),name = 'token_obtain_pair'),
    path('customer/', views.customerRegister, name="customer"),
    path('retailer/', views.retailerRegister, name = "retailer"),
]