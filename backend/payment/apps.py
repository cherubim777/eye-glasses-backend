from django.apps import AppConfig

# from .models import AdminAccount


class PaymentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payment"

    # def ready(self):
    #     admin_account, created = AdminAccount.objects.get_or_create()
