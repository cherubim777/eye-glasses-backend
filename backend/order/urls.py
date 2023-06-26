from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("placeOrder/", views.placeOrder, name="placeOrder"),
    path("placeCustomOrder/", views.placeCustomOrder, name="placeCustomOrder"),
    path(
        "getRetailerOrders/",
        views.GetRetailerOrders.as_view(),
        name="getRetailerOrders",
    ),
    path("orderFulfilled/<str:order_id>/", views.orderFulfilled, name="orderFulfilled"),
    path(
        "customOrderFulfilled/<str:order_id>/",
        views.CustomOrderFulfilled,
        name="customOrderFulfilled",
    ),
    path("placeCartOrder/", views.placeCartOrder, name="placeCartOrder"),
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
    path(
        "getCustomerOrders/",
        views.GetCustomerOrders.as_view(),
        name="getCustomerOrders",
    ),
    path(
        "markReady/<str:custom_order_id>/",
        views.markCustomOrderAsReady,
        name="markReady",
    ),
    path("numberOfOrders/", views.GetNumberOfOrders.as_view()),
    path("getStatNumbers/", views.GetStatNumbers.as_view(), name="getStatNumbers"),
]
