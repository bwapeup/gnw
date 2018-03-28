# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-28 07:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gnw', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateField(default=datetime.date.today)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gnw.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_type', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrollment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='enrollment.Enrollment_Type'),
        ),
    ]
