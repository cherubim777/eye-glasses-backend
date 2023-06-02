# from django.urls import path
# from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#     path('all/', CartListView.as_view(), name='cart-list'),
#     path('<str:user_name>/', CartDetailView.as_view(), name='cart-detail'),
# ]


from django.urls import path
from .views import CartListCreateAPIView, CartRetrieveUpdateDestroyAPIView, CartItemCreateAPIView, CartItemRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('carts/', CartListCreateAPIView.as_view(), name='cart-list-create'),
    path('carts/<int:pk>/', CartRetrieveUpdateDestroyAPIView.as_view(),
         name='cart-retrieve-update-destroy'),
    path('addcartitems/', CartItemCreateAPIView.as_view(), name='cart-item-create'),
    path('cartitems/<int:pk>/', CartItemRetrieveUpdateDestroyAPIView.as_view(),
         name='cart-item-retrieve-update-destroy'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
