# Generated by Django 3.2.5 on 2021-09-15 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0035_auto_20210913_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='graded',
            field=models.BooleanField(default=False),
        ),
    ]