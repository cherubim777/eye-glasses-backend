from django.db import models
from user.models import *


# Create your models here.
class SalesReport(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    number_of_products = models.IntegerField(default=0)
    total_number_of_products = models.IntegerField(default=0)
    total_number_of_orders = models.IntegerField(default=0)
    total_number_of_transaction = models.IntegerField(default=0)

    @staticmethod
    def create(retailer):
        sales = SalesReport.objects.create(retailer=retailer)
        return sales


class Report(models.Model):
    number_of_customers = models.IntegerField()
    number_of_retailers = models.IntegerField()
    total_number_of_products = models.IntegerField(default=0)
    total_number_of_orders = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
