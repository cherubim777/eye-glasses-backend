from django.db import models

from product.models import Product
from user.models import Customer, Retailer


# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200)

    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2)
    isPaid = models.BooleanField(default=True)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.createdAt.strftime('%Y-%m-%d %H:%M:%S')} - {self.customer.first_name} {self.customer.last_name} - {self.retailer.store_name}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    # image =

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.address


class CustomOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.SET_NULL, null=True)
    rightSphere = models.FloatField()
    leftSphere = models.FloatField()
    rightCylinder = models.FloatField()
    leftCylinder = models.FloatField()
    rightAxis = models.FloatField()
    leftAxis = models.FloatField()
    rightPrism = models.FloatField()
    leftPrism = models.FloatField()

    paymentMethod = models.CharField(max_length=200)

    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    isPaid = models.BooleanField(default=True)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    isReady = models.BooleanField(default=False)
    readyAt = models.DateTimeField(auto_now_add=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
