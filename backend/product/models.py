from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.

class Product(models.Model):
    retailer = models.ForeignKey(User, on_delete=models.SET_NULL ,null=True)
    product_id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    Type = models.CharField(max_length=50)
    #category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name
    
    
    
class ProductItem(models.Model):
    product_item_id = models.AutoField(primary_key=True, editable=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=200)
    photo = models.ImageField(null=True, blank=True)
    countInStock = models.IntegerField(default=0)
    gender_category = models.CharField(max_length=6)
    age_group = models.models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    color = models.CharField(20)
    createdAt = models.DateTimeField(auto_now_add=True)