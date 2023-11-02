# Generated by Django 4.2.6 on 2023-10-22 22:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0036_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='like',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]