from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    # description = models.TextField()
    # image = models.ImageField(
    #     upload_to='wishlist/images', blank=True, null=True)
    purchased = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
