# Generated by Django 4.2.1 on 2023-06-23 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='retaileraccount',
            name='retailer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.retailer'),
        ),
        migrations.AddField(
            model_name='customeraccount',
            name='customer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.customer'),
        ),
    ]
