# Generated by Django 4.2.1 on 2023-06-17 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_customorder_commisionrate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customorder',
            old_name='commisionRate',
            new_name='commisionPrice',
        ),
    ]
