# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-24 23:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Economy', '0007_auto_20161124_2339'),
        ('database', '0013_auto_20161121_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='discount_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='damages',
            name='repairedBy',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Economy.Employee'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='bikes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Bike'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='numberOfGuests',
            field=models.IntegerField(default=2, verbose_name='antal gäster'),
        ),
    ]