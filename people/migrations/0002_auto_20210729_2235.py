# Generated by Django 3.2.5 on 2021-07-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='mobile',
        ),
        migrations.AddField(
            model_name='customuser',
            name='mobile',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
