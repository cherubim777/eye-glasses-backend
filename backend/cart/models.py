from django.db import models

# cart/models.py
from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
