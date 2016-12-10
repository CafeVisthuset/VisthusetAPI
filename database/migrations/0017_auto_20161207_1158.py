# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-07 11:58
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0016_auto_20161126_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default=datetime.date.today, verbose_name='bokningsdatum'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='endDate',
            field=models.DateField(blank=True, null=True, verbose_name='datum för hemresa'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='guest',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='gäst'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='startDate',
            field=models.DateField(blank=True, null=True, verbose_name='datum för avresa'),
        ),
        migrations.AlterField(
            model_name='discount_codes',
            name='guest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='gäst'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='name',
            field=models.CharField(max_length=25, null=True, verbose_name='namn'),
        ),
        migrations.DeleteModel(
            name='Guest',
        ),
    ]
