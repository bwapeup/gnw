# Generated by Django 3.2.5 on 2021-09-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0031_alter_assignment_submitted_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
