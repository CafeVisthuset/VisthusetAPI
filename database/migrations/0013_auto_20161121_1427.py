# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-21 14:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_auto_20161112_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='damages',
            name='repairedBy',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]