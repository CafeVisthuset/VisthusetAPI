# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-27 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='guest',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='guest', to='database.Guest', verbose_name='gäst'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rooms',
            name='number',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='damages',
            name='bike_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='damages', to='database.Bike', verbose_name='Skada på cykel'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Pris för rum exkl. moms', max_digits=7, verbose_name='pris exkl. moms'),
        ),
    ]
