from django.db import models
# from django.contrib.auth.models import User
from product.models import Product
from user.models import Customer


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=("created at"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=("updated at"))

    def __str__(self):
        return f"{self.customer}'s Cart ({self.pk})"

    @staticmethod
    def create(customer=None):
        cart = Cart.objects.create(customer=customer)
        return cart


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items")
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=("product"))
    quantity = models.PositiveIntegerField(
        default=1, verbose_name=("quantity"))

    # @property
    def get_price(self):
        return self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product_id.name} in {self.cart}"
