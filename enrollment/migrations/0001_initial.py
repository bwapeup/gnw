# Generated by Django 3.2.5 on 2021-07-08 09:26

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
            name='Enrollment_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_type', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateField(default=datetime.date.today)),
                ('is_current', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gnw.course')),
                ('enrollment_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='enrollment.enrollment_type')),
            ],
        ),
    ]
