# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-22 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0012_auto_20161121_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='freezer',
            old_name='freezer_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='fridge',
            old_name='fridge_type',
            new_name='type',
        ),
        migrations.AlterUniqueTogether(
            name='fridge',
            unique_together=set([]),
        ),
    ]