# Generated by Django 4.2.1 on 2023-06-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='isFavourite',
            field=models.BooleanField(default=False),
        ),
    ]