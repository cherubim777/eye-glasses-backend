# Generated by Django 4.2.1 on 2023-06-17 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_rename_commisionrate_customorder_commisionprice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customorder',
            old_name='commisionPrice',
            new_name='commissionPrice',
        ),
    ]
