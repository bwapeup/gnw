# Generated by Django 3.2.5 on 2021-08-28 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gnw', '0023_auto_20210826_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_type',
            field=models.CharField(choices=[('VIDEO', 'Video'), ('QUIZ', 'Quiz'), ('ASSIGNMENT', 'Assignment')], max_length=25),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='')),
                ('lesson', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gnw.lesson')),
            ],
        ),
    ]
