# Generated by Django 4.2.1 on 2023-06-18 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('cart', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.customer'),
        ),
    ]