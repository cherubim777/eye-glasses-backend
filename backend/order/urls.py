from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("placeOrder/", views.placeOrder, name="placeOrder"),
    path("placeCustomOrder/", views.placeCustomOrder, name="placeCustomOrder"),
    path(
        "getRetailerOrders/",
        views.getRetailerOrders,
        name="getRetailerOrders",
    ),
    path("orderFulfilled/<str:order_id>/", views.orderFulfilled, name="orderFulfilled"),
    path(
        "customOrderFulfilled/<str:order_id>/",
        views.CustomOrderFulfilled,
        name="customOrderFulfilled",
    ),
    # path("getRetailerOrder/<str:pk>", views.getRetailerOrder, name="getRetailerOrder"),
    # path("placeCartOrder/", views.placeCartOrder, name="placeCartOrder"),
    path(
        "getCustomerCustomOrders/",
        views.getCustomerCustomOrders,
        name="getCustomerCustomOrder",
    ),
    path(
        "getRetailerCustomOrders/",
        views.getRetailerCustomOrders,
        name="getRetailCustomOrder",
    ),
    path("getCustomerOrders/", views.getCustomerOrders, name="getCustomerOrders"),
    path(
        "markReady/<str:custom_order_id>/",
        views.markCustomOrderAsReady,
        name="markReady",
    ),
]
