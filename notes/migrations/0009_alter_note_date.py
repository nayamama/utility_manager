# Generated by Django 3.2 on 2021-06-19 21:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 19, 21, 5, 7, 944651, tzinfo=utc)),
        ),
    ]