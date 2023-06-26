from django.contrib import admin
from .models import CustomerAccount, RetailerAccount, AdminAccount, Transaction

# Register your models here.
admin.site.register(CustomerAccount)
admin.site.register(RetailerAccount)
admin.site.register(AdminAccount)
admin.site.register(Transaction)
