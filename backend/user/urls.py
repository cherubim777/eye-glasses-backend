from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("customer/", views.customerRegister, name="customer"),
    path("retailer/", views.retailerRegister, name="retailer"),
    path("getAllCustomers/", views.getAllCustomers, name="getAllCustomers"),
    path("getAllRetailers/", views.getAllRetailers, name="getAllRetailers"),
    path("updateCustomer/", views.updateCustomer, name="updateCustomer"),
    path("updateRetailer/", views.updateCustomer, name="updateCustomer"),
    path("updateUser/", views.updateUser, name="updateUser"),
    path("deletAccount/", views.deleteAccount, name="deleteAccount"),
    path("getCustomerProfile/", views.getCustomerProfile, name="getCustomerProfile"),
    path("getRetailerProfile/", views.getRetailerProfile, name="getRetailerProfile"),
]
