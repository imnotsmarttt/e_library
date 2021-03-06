# Generated by Django 3.0.2 on 2022-07-17 09:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('country', models.CharField(max_length=255, verbose_name='Страна')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('mail', models.CharField(max_length=255, verbose_name='Отделение Новой Почты')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='coupons.Coupon')),
            ],
            options={
                'db_table': 'Order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кол-во')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='catalog.Product')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='orders.Order')),
            ],
            options={
                'db_table': 'OrderItem',
            },
        ),
    ]
