# Generated by Django 2.2.7 on 2022-08-22 13:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_auto_20220822_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appartament',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 8, 22, 13, 16, 18, 832302, tzinfo=utc), verbose_name='Дата объявления'),
        ),
    ]
