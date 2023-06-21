from django.contrib import admin
from django.urls import path, include
from . import views


from django.urls import path, include


urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("customer/", views.customerRegister, name="customer"),
    path("retailer/", views.retailerRegister, name="retailer"),
    path("getAllCustomers/", views.getAllCustomers, name="getAllCustomers"),
    path("getAllRetailers/", views.getAllRetailers, name="getAllRetailers"),
    path("updateCustomer/", views.updateCustomer, name="updateCustomer"),
    path("updateRetailer/", views.updateRetailer, name="updateRetailer"),
    path("updateUser/", views.updateUser, name="updateUser"),
    path("deletAccount/", views.deleteAccount, name="deleteAccount"),
    path(
        "getCustomerProfile/",
        views.GetCustomerProfile.as_view(),
        name="getCustomerProfile",
    ),
    path(
        "getRetailerProfile/",
        views.GetRetailerProfile.as_view(),
        name="getRetailerProfile",
    ),
    path("acceptCustom/", views.GetCustomOrderRetailer.as_view(), name="accceptCustom"),
    path("resetPassword/", views.reset_password, name="resetPassword"),
    path("confirmReset/", views.confirm_reset, name="confirmReset"),
    path(
        "getCustomerProfile/<str:id>",
        views.GetCustomerProfileById.as_view(),
        name="GetCustomerProfileById",
    ),
    path(
        "getRetailerProfile/<str:id>",
        views.GetRetailerProfileById.as_view(),
        name="GetRetailerProfileById",
    ),
]
