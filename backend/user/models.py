from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.contrib.auth.models import User


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
    photo = models.ImageField()
    accepts_custom_order = models.BooleanField(default=False)
    custom_order_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, default=500
    )
    store_name = models.CharField(max_length=200)
    # store_id = models.AutoField(primary_key=True, editable=False)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    reset_password_code = models.CharField(max_length=100, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def updateRating(self, rating):
        if rating is None:
            self.rating = Decimal(rating)

        else:
            self.rating = (Decimal(self.rating) + Decimal(rating)) / (
                self.numReviews + 1
            )

    def set_code(self, code):
        self.reset_password_code = code
        self.save()

    def __str__(self):
        return self.first_name
