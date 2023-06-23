from django.db import models
from user.models import *


# Create your models here.
class RetailerNotification(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)


class CustomerNotification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
