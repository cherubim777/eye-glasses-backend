from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from user.models import Customer


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def create(customer=None):
        cart = Cart.objects.create(customer=customer)
        return cart

    def __str__(self):
        return f"Cart for {self.customer.first_name} {self.customer.last_name}"
