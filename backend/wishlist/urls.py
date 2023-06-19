from django.urls import path
from .views import WishListItemView, WishListClearView

urlpatterns = [
    path('wishlist/', WishListItemView.as_view()),
    path('wishlist/<int:product_id>', WishListItemView.as_view()),
    path('clear/', WishListClearView.as_view()),

]
