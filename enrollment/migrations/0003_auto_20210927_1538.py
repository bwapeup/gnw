# Generated by Django 3.2.5 on 2021-09-27 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process_New_Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_details', models.JSONField()),
            ],
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='enrollment_type',
            field=models.CharField(choices=[('TRIAL', 'Trial'), ('REGULAR', 'regular')], max_length=100),
        ),
        migrations.DeleteModel(
            name='Enrollment_Type',
        ),
    ]
