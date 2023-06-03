from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

    def get_items(self):
        return WishlistItem.objects.filter(wishlist=self)

    def add_item(self, product):
        item, created = WishlistItem.objects.get_or_create(
            wishlist=self, product=product)
        return item

    def remove_item(self, product):
        WishlistItem.objects.filter(wishlist=self, product=product).delete()


class WishListItem(models.Model):
    wishlist = models.ForeignKey(
        WishList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} ({self.wishlist})"
