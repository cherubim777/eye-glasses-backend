# Generated by Django 4.2.1 on 2023-06-26 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('report', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesreport',
            name='retailer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.retailer'),
        ),
    ]
