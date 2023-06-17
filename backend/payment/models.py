from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from user.models import Customer, Retailer
from rest_framework.response import Response


# the following account model is written to simulate money transaction between customer and retailer
class Account(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, null=True, blank=True
    )
    retailer = models.OneToOneField(
        Retailer, on_delete=models.CASCADE, null=True, blank=True
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reserved_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_reserved_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, editable=False
    )

    def __str__(self):
        if self.customer:
            return f"Customer Account ({self.customer})"
        elif self.retailer:
            return f"Retailer Account ({self.retailer})"
        else:
            return "Account"

    def increase_balance(self, amount):
        self.balance += amount
        self.save()

    def decrease_balance(self, amount):
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.reserved_balance += amount
        self.total_reserved_balance += amount
        self.save()

    def fulfill_order(self, amount, retailer_account):
        if self.reserved_balance < amount:
            raise ValueError("Insufficient reserved balance")
        self.reserved_balance -= amount
        self.total_reserved_balance -= amount
        retailer_account.increase_balance(amount - amount * Decimal(0.02))
        amount = amount * Decimal(0.02)
        admin_account = AdminAccount.objects.first()
        admin_account.increase_balance(amount)
        self.save()
        retailer_account.save()
        return {"message": "money transferred to retailer account"}

    @staticmethod
    def create(customer=None, retailer=None, initial_balance=0):
        account = Account.objects.create(
            customer=customer, retailer=retailer, balance=initial_balance
        )
        return account


class AdminAccount(models.Model):
    _id = 1
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "AdminAccount"

    def increase_balance(self, amount):
        self.balance += amount
        self.save()
