# Generated by Django 4.2.6 on 2023-10-17 16:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0017_alter_newslitter_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslitter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 17, 16, 2, 35, 100005, tzinfo=datetime.timezone.utc)),
        ),
    ]
