from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("getRetailerAccount/", views.getRetailerAccount, name="getRetailerAccount"),
    path("getCustomerAccount/", views.getCustomerAccount, name="getCustomerAccountt"),
]
