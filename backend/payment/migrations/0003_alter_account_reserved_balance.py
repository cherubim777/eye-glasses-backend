# Generated by Django 4.2.1 on 2023-06-17 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='reserved_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]