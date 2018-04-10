# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-10 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=25)),
                ('session_key', models.CharField(max_length=40)),
                ('token_hex_str', models.CharField(max_length=32)),
                ('created', models.DateTimeField()),
                ('verified', models.BooleanField(default=False)),
                ('expired', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='sms_code',
            old_name='last_update',
            new_name='created',
        ),
        migrations.AddField(
            model_name='sms_code',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]
