# Generated by Django 4.2.1 on 2023-06-18 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_retailer_price_for_custom_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retailer',
            name='price_for_custom_order',
        ),
        migrations.AddField(
            model_name='retailer',
            name='custom_order_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=500, max_digits=7, null=True),
        ),
    ]
