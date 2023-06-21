from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("getProducts/", views.GetProducts.as_view(), name="getProducts"),
    path("getProduct/<str:pk>/", views.GetProduct.as_view(), name="getProduct"),
    path(
        "filterProducts/<str:q>/", views.FilterProducts.as_view(), name="filterProducts"
    ),
    path(
        "deleteProduct/<str:pk>/", views.DeleteProduct.as_view(), name="deleteProduct"
    ),
    path("addProduct/", views.AddProduct.as_view(), name="addProduct"),
    path(
        "getRetailerProducts/",
        views.GetRetailerProducts.as_view(),
        name="getRetailerProducts",
    ),
    path(
        "updateProduct/<str:pk>/", views.UpdateProduct.as_view(), name="updateProduct"
    ),
    path("addReview/<int:pk>/", views.addReview, name="addReview"),
    path("getReviews/<str:pk>/", views.getReviews, name="getReviews"),
    path("getLatest/", views.GetLatest.as_view(), name="getLatest"),
    path("getPopular/", views.GetPopular.as_view(), name="getFeatured"),
    path("getFeatured/", views.GetFeatured.as_view(), name="getFeatured"),
]
