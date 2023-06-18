# Generated by Django 4.2.1 on 2023-06-17 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Aviator', 'Aviator'), ('Wayfarer', 'Wayfarer'), ('Round', 'Round'), ('Cat Eye', 'Cat Eye'), ('Sports', 'Sports'), ('Oversized', 'Oversized'), ('Mirrored', 'Mirrored'), ('Polarized', 'Polarized'), ('Gradient', 'Gradient'), ('Clip-On', 'Clip-On')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age_group', models.CharField(choices=[('K', 'Kids'), ('T', 'Teens'), ('A', 'Adults'), ('S', 'Seniors')], default='A', max_length=1)),
                ('gender_category', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')], default='U', max_length=1)),
                ('category', models.CharField(blank=True, choices=[('Aviator', 'Aviator'), ('Wayfarer', 'Wayfarer'), ('Round', 'Round'), ('Cat Eye', 'Cat Eye'), ('Sports', 'Sports'), ('Oversized', 'Oversized'), ('Mirrored', 'Mirrored'), ('Polarized', 'Polarized'), ('Gradient', 'Gradient'), ('Clip-On', 'Clip-On')], max_length=20, null=True)),
                ('brand', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('numReviews', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('photo', models.ImageField(default='photo', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countInStock', models.IntegerField(default=0)),
                ('size', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=20)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('comment', models.TextField()),
            ],
        ),
    ]
