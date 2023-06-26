import calendar
from decimal import Decimal
from django.db.models import Sum
from django.db import models
from django.db.models import DecimalField
from user.models import *
import datetime
from payment.models import Transaction
from django.db.models.functions import ExtractMonth
from user.models import Retailer
from django.db.models import Count
import json
from product.models import Product

# Create your models here.


class MonthlyRevenue(models.CharField):
    def __init__(self, *args, **kwargs):
        default_sales = kwargs.pop("default", {})
        self.sales = {
            "January": Decimal("0.00"),
            "February": Decimal("0.00"),
            "March": Decimal("0.00"),
            "April": Decimal("0.00"),
            "May": Decimal("0.00"),
            "June": Decimal("0.00"),
            "July": Decimal("0.00"),
            "August": Decimal("0.00"),
            "September": Decimal("0.00"),
            "October": Decimal("0.00"),
            "November": Decimal("0.00"),
            "December": Decimal("0.00"),
        }
        self.sales.update(default_sales)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.sales != {
            "January": Decimal("0.00"),
            "February": Decimal("0.00"),
            "March": Decimal("0.00"),
            "April": Decimal("0.00"),
            "May": Decimal("0.00"),
            "June": Decimal("0.00"),
            "July": Decimal("0.00"),
            "August": Decimal("0.00"),
            "September": Decimal("0.00"),
            "October": Decimal("0.00"),
            "November": Decimal("0.00"),
            "December": Decimal("0.00"),
        }:
            kwargs["default"] = self.sales
        return name, path, args, kwargs

    def db_type(self, connection):
        return "varchar(100)"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        value_str = str(value)
        if "," in value_str:
            sales_str = value_str.split(",")
            sales = {
                m: Decimal(s) for m, s in [s.split(":") for s in sales_str.split(";")]
            }
            return MonthlyRevenue(sales=sales)
        else:
            return MonthlyRevenue(sales={})

    def to_python(self, value):
        if isinstance(value, MonthlyRevenue):
            return value.sales
        if value is None:
            return None
        value_str = str(value)
        sales_str = value_str.split(",")
        sales = {m: Decimal(s) for m, s in [s.split(":") for s in sales_str.split(";")]}
        return sales

    def get_prep_value(self, value):
        if value is None:
            return None
        sales = value
        sales_str = ";".join([f"{m}:{s}" for m, s in sales.items()])
        return f"{sales_str}"


class SalesReport(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    current_year_revenue = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    last_year_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    number_of_orders_completed = models.IntegerField(default=0)
    total_number_of_transaction = models.IntegerField(default=0)
    monthly_revenues = models.TextField(default="[]")
    number_of_products = models.IntegerField(default=0)

    def __str__(self):
        return f"Sales report of {self.retailer.store_name}"

    @staticmethod
    def create(retailer):
        sales_report = SalesReport.objects.create(retailer=retailer)
        return sales_report

    def update(self, retailer):
        # Get the current year
        current_year = datetime.datetime.now().year

        # Get the start and end dates of the current year and the last year
        start_date_current_year = datetime.datetime(current_year, 1, 1)
        end_date_current_year = datetime.datetime(current_year, 12, 31, 23, 59, 59)
        start_date_last_year = datetime.datetime(current_year - 1, 1, 1)
        end_date_last_year = datetime.datetime(current_year - 1, 12, 31, 23, 59, 59)

        # Aggregate the transaction amounts by month for the current year and the last year
        current_year_monthly_sales = (
            Transaction.objects.filter(
                retailer=retailer,
                createdAt__gte=start_date_current_year,
                createdAt__lte=end_date_current_year,
            )
            .annotate(month=ExtractMonth("createdAt"))
            .values("month")
            .annotate(
                total_sales=Coalesce(
                    Sum("amount", output_field=models.DecimalField()), Decimal("0.00")
                )
            )
            .order_by("month")
        )

        last_year_monthly_sales = (
            Transaction.objects.filter(
                retailer=retailer,
                createdAt__gte=start_date_last_year,
                createdAt__lte=end_date_last_year,
            )
            .annotate(month=ExtractMonth("createdAt"))
            .values("month")
            .annotate(
                total_sales=Coalesce(
                    Sum("amount", output_field=models.DecimalField()), Decimal("0.00")
                )
            )
            .order_by("month")
        )

        # Update the current year and last year revenue fields
        self.current_year_revenue = current_year_monthly_sales.aggregate(
            total_sales=Coalesce(
                Sum("total_sales", output_field=models.DecimalField()), Decimal("0.00")
            )
        )["total_sales"]

        self.last_year_revenue = last_year_monthly_sales.aggregate(
            total_sales=Coalesce(
                Sum("total_sales", output_field=models.DecimalField()), Decimal("0.00")
            )
        )["total_sales"]

        # Update the monthly sales amounts in the monthly_revenues list
        monthly_revenues = []
        for month_number in range(1, 13):
            month_name = calendar.month_name[month_number]
            current_year_month_sales = next(
                (
                    sales
                    for sales in current_year_monthly_sales
                    if sales["month"] == month_number
                ),
                {"total_sales": Decimal("0.00")},
            )
            last_year_month_sales = next(
                (
                    sales
                    for sales in last_year_monthly_sales
                    if sales["month"] == month_number
                ),
                {"total_sales": Decimal("0.00")},
            )
            monthly_revenues.append(
                {
                    "month": month_number,
                    "month_name": month_name,
                    "current_year_revenue": str(
                        current_year_month_sales["total_sales"]
                    ),
                    "last_year_revenue": str(last_year_month_sales["total_sales"]),
                }
            )
        self.monthly_revenues = json.dumps(monthly_revenues)

        # Update the total sales, number_of_orders_completed, and total_number_of_transaction fields
        self.total_sales = Transaction.objects.filter(retailer=retailer).aggregate(
            total_sales=Coalesce(
                Sum(
                    "amount",
                    output_field=models.DecimalField(max_digits=10, decimal_places=2),
                ),
                Decimal("0.00"),
                output_field=models.DecimalField(max_digits=10, decimal_places=2),
            )
        )["total_sales"]

        self.number_of_orders_completed = Transaction.objects.filter(
            retailer=retailer
        ).count()

        self.total_number_of_transaction = Transaction.objects.filter(
            retailer=retailer
        ).aggregate(total_transaction=Count("id"))["total_transaction"]

        # Save the SalesReport instance
        self.save()

    def update_no_of_products(self):
        retailer = self.retailer
        self.number_of_products = Product.objects.filter(retailer=retailer).aggregate(
            number_of_products=Coalesce(
                Sum(
                    "quantity",
                    output_field=models.IntegerField(),
                ),
                Decimal("0.00"),
                output_field=models.DecimalField(max_digits=10, decimal_places=2),
            )
        )["number_of_products"]
        self.save()
