# Generated by Django 3.2 on 2021-04-18 02:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('util_calculator', '0002_auto_20210409_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bill_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='bill',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 18, 2, 24, 0, 296914, tzinfo=utc), verbose_name='data filled'),
        ),
    ]