# Generated by Django 3.2.5 on 2021-09-13 07:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0034_auto_20210913_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='assignment',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='assignment',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='assignment',
            name='image6',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='assignment',
            name='image7',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='assignment',
            name='image8',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='submitted_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]