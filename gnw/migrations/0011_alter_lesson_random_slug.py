# Generated by Django 3.2.5 on 2021-07-31 03:52

from django.db import migrations, models
import gnw.models


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0010_alter_lesson_random_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='random_slug',
            field=models.CharField(default=gnw.models.Lesson.random_id_generator, editable=False, max_length=6, unique=True),
        ),
    ]
