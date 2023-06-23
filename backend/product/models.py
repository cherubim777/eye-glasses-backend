from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User, Group
from user.models import Retailer, Customer
from django.db.models.functions import Coalesce


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

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
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
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True
    )
    brand = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, default=0
    )
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=20, default="46-20-145 B40-Medium")
    numReviews = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(default="photo")

    def decrease_quantity(self, amount=1):
        amount = int(amount)
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
            return True
        else:
            return False

    def calculateRating(self, rating):
        if rating == None:
            self.rating = self.rating
        else:
            self.rating = (Decimal(self.rating) + Decimal(rating)) / (
                self.numReviews + 1
            )
            self.numReviews += 1

        self.retailer.updateRating(self.rating)
        self.save()

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    countInStock = models.IntegerField(default=0)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} given to product {self.product.name} by {self.customer.first_name}"
