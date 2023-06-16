from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("placeOrder/", views.placeOrder, name="placeOrder"),
    path(
        "getRetailerNotCustomOrder/",
        views.getRetailerNotCustomrOrders,
        name="getRetailerNotCustomOrder",
    )
    # path("getRetailerOrder/<str:pk>", views.getRetailerOrder, name="getRetailerOrder"),
    # path("placeCartOrder/", views.placeCartOrder, name="placeCartOrder"),
]
