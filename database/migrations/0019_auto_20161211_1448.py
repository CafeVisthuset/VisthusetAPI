# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-11 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_auto_20161210_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomsAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AccomodationBooking',
            fields=[
            ],
            options={
                'verbose_name': 'boendebokning',
                'proxy': True,
                'verbose_name_plural': 'bokningar boende',
            },
            bases=('database.booking',),
        ),
        migrations.AlterModelOptions(
            name='bikeavailable',
            options={'verbose_name': 'tillgänglighet cykel', 'verbose_name_plural': 'tillgänglighet cyklar'},
        ),
        migrations.AlterModelOptions(
            name='rooms',
            options={'ordering': ['owned_by'], 'verbose_name': 'rum', 'verbose_name_plural': 'rum'},
        ),
        migrations.AddField(
            model_name='booking',
            name='type',
            field=models.CharField(choices=[('B', 'Cykel'), ('A', 'Boende'), ('L', 'Lunch'), ('P', 'Paket'), ('E', 'Event')], default='B', max_length=25),
        ),
        migrations.AddField(
            model_name='roomsavailable',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='database.Rooms'),
        ),
    ]
