# Generated by Django 4.2.6 on 2023-12-17 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0010_remove_coupon_max_number_remove_coupon_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='expiration_date',
        ),
    ]
