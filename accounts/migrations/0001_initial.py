# Generated by Django 4.2.6 on 2023-12-07 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='users/')),
                ('about', models.TextField(blank=True, max_length=4000, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('address_line_1', models.CharField(blank=True, max_length=50)),
                ('address_line_2', models.CharField(blank=True, max_length=50)),
                ('fb_link', models.URLField(blank=True, null=True)),
                ('twitter_link', models.URLField(blank=True, null=True)),
                ('instagram_link', models.URLField(blank=True, null=True)),
                ('linked_in_link', models.URLField(blank=True, null=True)),
                ('headline', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
