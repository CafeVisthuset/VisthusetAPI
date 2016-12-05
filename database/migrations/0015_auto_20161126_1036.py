# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-26 10:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Economy', '0007_auto_20161124_2339'),
        ('database', '0014_auto_20161124_2339'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bike',
            options={'ordering': ['id'], 'verbose_name': 'cykel', 'verbose_name_plural': 'cyklar'},
        ),
        migrations.AlterModelOptions(
            name='damages',
            options={'ordering': ['repaired', 'discoveredDate'], 'verbose_name': 'skada', 'verbose_name_plural': 'skador'},
        ),
        migrations.AddField(
            model_name='damages',
            name='discoveredBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Discovered_by', to='Economy.Employee', verbose_name='upptäckt av'),
        ),
        migrations.AddField(
            model_name='damages',
            name='discoveredDate',
            field=models.DateField(default=datetime.date.today, verbose_name='Skada upptäckt'),
        ),
        migrations.AddField(
            model_name='damages',
            name='repairedDate',
            field=models.DateField(default=datetime.date.today, verbose_name='Skada reparerad'),
        ),
        migrations.RemoveField(
            model_name='booking',
            name='bikes',
        ),
        migrations.AddField(
            model_name='booking',
            name='bikes',
            field=models.ManyToManyField(to='database.Bike'),
        ),
        migrations.AlterField(
            model_name='damages',
            name='bike_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Bike', verbose_name='Skada på cykel'),
        ),
        migrations.AlterField(
            model_name='damages',
            name='damageType',
            field=models.CharField(max_length=200, verbose_name='beskrivning av skada'),
        ),
        migrations.AlterField(
            model_name='damages',
            name='repaired',
            field=models.BooleanField(default=False, verbose_name='lagad (J/N)'),
        ),
        migrations.AlterField(
            model_name='damages',
            name='repairedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repaired_by', to='Economy.Employee', verbose_name='lagad av'),
        ),
    ]