# Generated by Django 3.2 on 2021-06-21 19:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('util_calculator', '0009_alter_bill_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 21, 19, 16, 43, 268634, tzinfo=utc), verbose_name='data filled'),
        ),
    ]
