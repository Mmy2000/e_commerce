# Generated by Django 4.2.6 on 2023-10-14 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_product_aroduct_accessories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='aroduct_accessories',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_accessories', to='product.productcategory', verbose_name='product_accessories'),
        ),
    ]
