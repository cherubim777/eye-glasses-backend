from django.urls import path
from .views import WishListView  # WishListDetailView

urlpatterns = [
    path('wishlist/', WishListView.as_view()),
    path('wishlist/<int:item_id>/', WishListView.as_view()),

]
