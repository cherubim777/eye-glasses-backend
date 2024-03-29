from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, null=False, on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    local_address = models.CharField(max_length=30)
    subcity = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    photo = models.ImageField(null=True, blank=True)
    reset_password_code = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def set_code(self, code):
        self.reset_password_code = code
        self.save()


class Retailer(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, null=False, on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    local_address = models.CharField(max_length=30)
    subcity = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    photo = models.ImageField(null=True, blank=True)
    accepts_custom_order = models.BooleanField(default=False)
    custom_order_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, default=500
    )
    store_name = models.CharField(max_length=200)

    rating = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    reset_password_code = models.CharField(max_length=100, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def updateRating(self, rating):
        if self.rating == 0:
            self.rating = rating
        else:
            self.rating = (Decimal(self.rating) + Decimal(rating)) / 2

        self.save()

    def set_code(self, code):
        self.reset_password_code = code
        self.save()

    def __str__(self):
        return self.first_name
