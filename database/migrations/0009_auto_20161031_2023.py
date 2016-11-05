# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-31 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20161031_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikesbooking',
            name='bikes',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='database.Bike'),
        ),
        migrations.AddField(
            model_name='bikesbooking',
            name='numberOfGuests',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='bikesbooking',
            name='bookingDate',
            field=models.DateField(verbose_name='Date of booking'),
        ),
    ]