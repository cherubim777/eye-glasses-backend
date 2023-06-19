# Generated by Django 4.2.1 on 2023-06-18 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlistitem',
            old_name='product',
            new_name='product_id',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='customer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.customer'),
            preserve_default=False,
        ),
    ]