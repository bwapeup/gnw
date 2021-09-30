# Generated by Django 3.2.5 on 2021-09-11 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0026_auto_20210907_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gnw.lesson'),
        ),
    ]