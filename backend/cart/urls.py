from django.urls import path
from .views import *

urlpatterns = [
    path('carts/', CartView.as_view(), name='cart'),
    path('delete/<int:product_id>/',
         CartItemDeleteView.as_view(), name='cart-item-delete'),
]
