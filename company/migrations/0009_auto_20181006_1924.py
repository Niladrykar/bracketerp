# Generated by Django 2.0.6 on 2018-10-06 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_auto_20181006_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='End_Date',
        ),
        migrations.RemoveField(
            model_name='company',
            name='Start_Date',
        ),
    ]
