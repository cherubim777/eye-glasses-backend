# Generated by Django 4.2.1 on 2023-06-18 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('product', '0003_remove_review_user_review_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='retailer',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='user.retailer'),
            preserve_default=False,
        ),
    ]