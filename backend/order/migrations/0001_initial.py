# Generated by Django 4.2.1 on 2023-06-23 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rightSphere', models.FloatField()),
                ('leftSphere', models.FloatField()),
                ('rightCylinder', models.FloatField()),
                ('leftCylinder', models.FloatField()),
                ('rightAxis', models.FloatField()),
                ('leftAxis', models.FloatField()),
                ('rightPrism', models.FloatField()),
                ('leftPrism', models.FloatField()),
                ('paymentMethod', models.CharField(max_length=200)),
                ('shippingPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('totalPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('commissionPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('delivery', models.CharField(choices=[('GO Delivery Ethiopia', 'GO Delivery Ethiopia'), ('WeDeliver', 'WeDeliver'), ('Eshi Express', 'Eshi Express'), ('Awra Delivery', 'Awra Delivery')], default='GO Delivery Ethiopia', max_length=20)),
                ('isPaid', models.BooleanField(default=True)),
                ('paidAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('isReady', models.BooleanField(default=False)),
                ('readyAt', models.DateTimeField(blank=True, null=True)),
                ('isDelivered', models.BooleanField(default=False)),
                ('deliveredAt', models.DateTimeField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentMethod', models.CharField(max_length=200)),
                ('delivery', models.CharField(choices=[('GO Delivery Ethiopia', 'GO Delivery Ethiopia'), ('WeDeliver', 'WeDeliver'), ('Eshi Express', 'Eshi Express'), ('Awra Delivery', 'Awra Delivery')], default='GO Delivery Ethiopia', max_length=20)),
                ('shippingPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('commissionRate', models.CharField(default='2%', max_length=5)),
                ('commissionPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('isPaid', models.BooleanField(default=True)),
                ('paidAt', models.DateTimeField(blank=True, null=True)),
                ('isDelivered', models.BooleanField(default=False)),
                ('deliveredAt', models.DateTimeField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('shippingPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('content_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('qty', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.order')),
            ],
        ),
    ]
