# Generated by Django 3.2 on 2021-06-22 02:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('util_calculator', '0010_alter_bill_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 2, 28, 22, 82237, tzinfo=utc), verbose_name='data filled'),
        ),
    ]
