# Generated by Django 3.2.5 on 2021-07-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0008_auto_20210722_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz_question',
            name='media_file_type',
            field=models.CharField(choices=[('AUDIO', 'Audio'), ('IMAGE', 'Image'), ('NONE', 'None')], default='NONE', max_length=20),
        ),
    ]
