from django.db import models
from user.models import *


# Create your models here.
class RetailerNotification(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"notification for retailer {self.retailer.first_name} {self.retailer.last_name}"


class CustomerNotification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"notification for customer {self.customer.first_name} {self.customer.last_name}"
