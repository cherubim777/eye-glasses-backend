# Generated by Django 4.2.1 on 2023-06-25 02:37

from django.db import migrations
import report.models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_rename_current_year_annual_revenue_salesreport_current_year_revenue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesreport',
            name='monthly_revenue',
            field=report.models.MonthlyRevenue(),
        ),
    ]