# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-12 09:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20161031_2023'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cashier',
        ),
        migrations.RemoveField(
            model_name='cleanday',
            name='Employee_id',
        ),
        migrations.RemoveField(
            model_name='cleanday',
            name='cleanPoint_id',
        ),
        migrations.DeleteModel(
            name='CleanDay',
        ),
        migrations.DeleteModel(
            name='CleanPoint',
        ),
    ]