from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# from user.models import Customer


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=("created at"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=("updated at"))

    def __str__(self):
        return f"{self.user}'s Cart ({self.pk})"

    @staticmethod
    def create(user=None):
        cart = Cart.objects.create(user=user)
        return cart


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=("product"))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=("quantity"))

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"
