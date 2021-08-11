# Generated by Django 3.2.5 on 2021-07-31 05:54

from django.db import migrations, models
import gnw.models


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0012_auto_20210731_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_number',
            field=models.PositiveIntegerField(default=gnw.models.Lesson.generate_lesson_order_number, help_text='Use default value unless recordering lessons', unique=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_number',
            field=models.PositiveIntegerField(default=gnw.models.Unit.generate_unit_order_number, help_text='Use default value unless reordering units', unique=True),
        ),
    ]