# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-02 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0002_cleanday_describtion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cleantask',
            old_name='day',
            new_name='cleanday',
        ),
        migrations.AlterField(
            model_name='cleanday',
            name='day',
            field=models.DateField(verbose_name='Clean_day'),
        ),
    ]