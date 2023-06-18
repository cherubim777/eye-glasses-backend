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
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


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
    price_for_custom_order = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    store_name = models.CharField(max_length=200)
    # store_id = models.AutoField(primary_key=True, editable=False)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def updateRating(self, rating):
        if rating is None:
            self.rating = rating

        else:
            self.rating = (self.rating + rating) / 2

    def __str__(self):
        return self.first_name
