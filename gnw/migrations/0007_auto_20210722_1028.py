# Generated by Django 3.2.5 on 2021-07-22 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0006_auto_20210721_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='mc_question',
        ),
        migrations.AddField(
            model_name='quiz_question',
            name='quiz',
            field=models.ManyToManyField(to='gnw.Quiz'),
        ),
    ]
