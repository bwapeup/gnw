# Generated by Django 3.2.5 on 2021-09-16 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0037_auto_20210916_1654'),
        ('progress', '0004_alter_completed_lessons_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='completed_lessons',
            name='assignment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gnw.assignment'),
        ),
    ]