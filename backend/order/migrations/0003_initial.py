# Generated by Django 4.2.1 on 2023-06-18 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0002_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='retailer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.retailer'),
        ),
        migrations.AddField(
            model_name='customorder',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.customer'),
        ),
        migrations.AddField(
            model_name='customorder',
            name='retailer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.retailer'),
        ),
    ]
