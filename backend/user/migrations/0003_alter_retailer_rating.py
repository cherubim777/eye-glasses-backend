# Generated by Django 4.2.1 on 2023-06-19 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_retailer_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailer',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]