from django.db import models
from django.utils import timezone
from decimal import Decimal
from order.models import Order, OrderItem
from product.models import Product
from user.models import Retailer


class Analytics(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    annual_revenue_last_year = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    annual_revenue_this_year = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    monthly_revenue = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    number_of_orders_completed = models.IntegerField(default=0)
    number_of_products_sold = models.IntegerField(default=0)

    @classmethod
    def calculate_revenue_metrics(cls, retailer):
        # Get the current date and the dates for the start of the last year and the start of the current year
        today = timezone.now().date()
        last_year_start = today.replace(year=today.year - 1, month=1, day=1)
        this_year_start = today.replace(month=1, day=1)
        this_month_start = today.replace(day=1)

        # Calculate the revenue metrics for the last year and the current year
        last_year_revenue = Decimal('0.00')
        this_year_revenue = Decimal('0.00')
        monthly_revenue = Decimal('0.00')

        orders = Order.objects.filter(
            retailer=retailer, createdAt=last_year_start)
        for order in orders:
            order_item = OrderItem.objects.get(order=order)
            if order.paidAt >= this_year_start:
                this_year_revenue += sum(order_item.price * order_item.qty)
            elif order.paidAt >= this_month_start:
                monthly_revenue += sum(order_item.price * order_item.qty)
            else:
                last_year_revenue += sum(order_item.price * order_item.qty)

        # Calculate the number of completed orders and products sold
        num_orders = orders.count()
        num_products = sum(order.num_items for order in orders)

        # Return the calculated metrics as a dictionary
        return {
            'annual_revenue_last_year': last_year_revenue,
            'annual_revenue_this_year': this_year_revenue,
            'monthly_revenue': monthly_revenue,
            'number_of_orders_completed': num_orders,
            'number_of_products_sold': num_products,
        }

    @classmethod
    def calculate_product_metrics(cls, retailer):
        # Get the products sold by the retailer in the last year
        today = timezone.now().date()
        last_year_start = today.replace(year=today.year - 1, month=1, day=1)
        products = Product.objects.filter(
            order__retailer=retailer, order__date_completed__gte=last_year_start)

        # Calculate the total revenue and number of products sold for each product
        product_metrics = {}
        for product in products:
            revenue = sum(order_item.price * order_item.quantity for order_item in product.orderitem_set.filter(
                order__retailer=retailer, order__date_completed__gte=last_year_start))
            num_sold = sum(order_item.quantity for order_item in product.orderitem_set.filter(
                order__retailer=retailer, order__date_completed__gte=last_year_start))
            product_metrics[product.name] = {
                'total_revenue': revenue,
                'number_sold': num_sold,
            }

        # Return the calculated metrics as a dictionary
        return product_metrics

    @staticmethod
    def create(retailer=None):
        analytics = Analytics.objects.create(retailer=retailer)
        return analytics
