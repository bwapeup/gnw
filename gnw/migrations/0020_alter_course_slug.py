# Generated by Django 3.2.5 on 2021-08-07 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0019_auto_20210803_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(help_text='Enter a URL-friendly course name without spaces and using only letters, digits, hypens, and underscores; leave it blank to auto generate from course name', max_length=200, unique=True),
        ),
    ]
