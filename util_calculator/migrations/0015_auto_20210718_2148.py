# Generated by Django 3.2 on 2021-07-19 01:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('util_calculator', '0014_auto_20210629_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 1, 48, 1, 457539, tzinfo=utc), verbose_name='data filled'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='utility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='util_calculator.utility'),
        ),
    ]
