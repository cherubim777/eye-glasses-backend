from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        CUSTOMER = "CUSTOMER", 'Customer'
        RETAILER = "RETAILER", 'Retailer'
        
    base_role = Role.ADMIN
    
    role = models.CharField(max_length=50, choices=Role.choices)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save( *args, **kwargs)
        
class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(self, *args, **kwargs)
        return results.filter(role = User.Role.CUSTOMER)
       
    
    
class Customer(User):
    base_role = User.Role.CUSTOMER
    customer = CustomerManager()
    
    class Meta:
        proxy = True
    
    def welcome(self):
        return "only for customers"
    
    
@@receiver(post_save, sender=Customer)
def create_user_profile(sender, instace, created, **kwargs):
    if created and instace.role == "CUSTOMER":
        CustomerProfile.objects.create(user = instace )
    

    
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Customer_id = models.AutoField()
    
    
class RetailerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(self, *args, **kwargs)
        return results.filter(role = User.Role.RETAILER)
       
    
    
class Retailer(User):
    base_role = User.Role.RETAILER
    retailer = RetailerManager()
    
    class Meta:
        proxy = True
    
    def welcome(self):
        return "only for retailers"