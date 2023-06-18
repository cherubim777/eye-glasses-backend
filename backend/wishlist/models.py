from django.db import models
# from django.contrib.auth.models import User
from user.models import Customer
from product.models import Product


class WishList(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer}'s Wishlist"

    # def get_items(self):
    #     return WishList.objects.filter(wishlist=self)
    def get_items(self):
        return self.items.all()

    def add_item(self, product_id):
        item = WishListItem.objects.create(
            wishlist=self, product_id=product_id)
        return item

    def remove_item(self, product_id):
        WishListItem.objects.filter(
            wishlist=self, product_id=product_id).delete()

    def clear(self):
        WishListItem.objects.filter(wishlist=self).delete()

    @staticmethod
    def create(customer=None):
        wishlist = WishList.objects.create(customer=customer)
        return wishlist


class WishListItem(models.Model):
    wishlist = models.ForeignKey(
        WishList, on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_id} ({self.wishlist})"
