# Generated by Django 4.2.1 on 2023-06-24 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='object_id',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='customOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.customorder'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
    ]
