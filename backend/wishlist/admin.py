from django.contrib import admin
from .models import WishList, WishListItem

# Register your models here.
admin.site.register(WishList)
admin.site.register(WishListItem)
