from django.contrib import admin
from .models import Product, Review, ProductItem, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductItem)
admin.site.register(Review)
admin.site.register(Category)
