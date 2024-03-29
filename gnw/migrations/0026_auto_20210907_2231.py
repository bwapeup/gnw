# Generated by Django 3.2.5 on 2021-09-07 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gnw', '0025_auto_20210906_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='graded_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='submitted_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='people.customuser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='assignment_details',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='lesson',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='gnw.lesson'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='random_slug',
            field=models.CharField(blank=True, help_text='Leave blank to use system default', max_length=6, unique=True),
        ),
    ]
