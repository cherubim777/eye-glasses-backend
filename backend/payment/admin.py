from django.contrib import admin
from .models import Account, AdminAccount

# Register your models here.
admin.site.register(Account)
admin.site.register(AdminAccount)
