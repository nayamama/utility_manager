# Generated by Django 3.2 on 2021-07-29 04:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('util_calculator', '0015_auto_20210718_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 4, 57, 5, 758987, tzinfo=utc), verbose_name='data filled'),
        ),
    ]