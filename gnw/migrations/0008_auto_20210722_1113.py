# Generated by Django 3.2.5 on 2021-07-22 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0007_auto_20210722_1028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz_question',
            old_name='content_option_1',
            new_name='option_1',
        ),
        migrations.RenameField(
            model_name='quiz_question',
            old_name='content_option_2',
            new_name='option_2',
        ),
        migrations.RenameField(
            model_name='quiz_question',
            old_name='content_option_3',
            new_name='option_3',
        ),
        migrations.RenameField(
            model_name='quiz_question',
            old_name='content_option_4',
            new_name='option_4',
        ),
    ]
