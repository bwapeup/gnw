# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-01 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0005_auto_20180501_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='is_current',
            field=models.BooleanField(default=True),
        ),
    ]
