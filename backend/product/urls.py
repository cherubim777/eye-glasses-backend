from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("getProducts/", views.getProducts, name="getProducts"),
    path("filterProducts/<str:q>/", views.filterProducts, name="filterProducts"),
    path(
        "deleteProduct/<str:pk>/", views.DeleteProduct.as_view(), name="deleteProduct"
    ),
    path("addProduct/", views.AddProduct.as_view(), name="addProduct"),
    path(
        "getRetailerProducts/",
        views.GetRetailerProducts.as_view(),
        name="getRetailerProducts",
    ),
    path("updateReview/<str:pk>/", views.UpdateProduct.as_view(), name="updateProduct"),
    path("addReview/<int:pk>/", views.addReview, name="addReview"),
    path(
        "productReviews/<int:pk>", views.ProductReviews.as_view(), name="productReviews"
    ),
]
