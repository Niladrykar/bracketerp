# Generated by Django 2.0.6 on 2018-11-01 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockkeeping', '0007_auto_20181101_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='Amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='rate',
            field=models.PositiveIntegerField(),
        ),
    ]
