# Generated by Django 4.2.6 on 2023-11-25 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_zip_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]