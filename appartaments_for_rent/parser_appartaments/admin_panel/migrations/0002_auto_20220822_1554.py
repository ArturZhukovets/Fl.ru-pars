# Generated by Django 2.2.7 on 2022-08-22 12:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appartament',
            options={'verbose_name': 'Квартира', 'verbose_name_plural': 'Квартиры'},
        ),
        migrations.AlterField(
            model_name='appartament',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 8, 22, 12, 54, 41, 711238, tzinfo=utc), verbose_name='Дата объявления'),
        ),
    ]