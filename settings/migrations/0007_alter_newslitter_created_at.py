# Generated by Django 4.2.6 on 2023-10-16 16:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_alter_newslitter_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslitter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 16, 39, 27, 115658, tzinfo=datetime.timezone.utc)),
        ),
    ]
