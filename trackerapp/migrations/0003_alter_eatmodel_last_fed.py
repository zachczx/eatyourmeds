# Generated by Django 4.2.7 on 2023-11-17 12:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackerapp', '0002_eatmodel_last_fed_alter_eatmodel_medicine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eatmodel',
            name='last_fed',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 17, 12, 4, 10, 488977, tzinfo=datetime.timezone.utc)),
        ),
    ]
