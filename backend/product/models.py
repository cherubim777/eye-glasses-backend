from django.db import models
from django.contrib.auth.models import User, Group
from user.models import Retailer


# Create your models here.


class Category(models.Model):
    CATEGORY_CHOICES = [
        ("Aviator", "Aviator"),
        ("Wayfarer", "Wayfarer"),
        ("Round", "Round"),
        ("Cat Eye", "Cat Eye"),
        ("Sports", "Sports"),
        ("Oversized", "Oversized"),
        ("Mirrored", "Mirrored"),
        ("Polarized", "Polarized"),
        ("Gradient", "Gradient"),
        ("Clip-On", "Clip-On"),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)


class Product(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("U", "Unisex"),
    ]

    AGE_GROUP_CHOICES = [
        ("K", "Kids"),
        ("T", "Teens"),
        ("A", "Adults"),
        ("S", "Seniors"),
    ]

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False)
    age_group = models.CharField(max_length=1, choices=AGE_GROUP_CHOICES, default="A")
    gender_category = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="U"
    )
    # category = models.ForeignKey(
    #     Category, null=True, blank=True, on_delete=models.SET_NULL
    # )
    brand = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(default="photo")

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    countInStock = models.IntegerField(default=0)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.rating)
