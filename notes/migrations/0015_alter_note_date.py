# Generated by Django 3.2 on 2021-06-29 20:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0014_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 29, 20, 0, 28, 60281, tzinfo=utc)),
        ),
    ]
