# Generated by Django 2.0.6 on 2018-11-01 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockkeeping', '0008_auto_20181101_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_total',
            name='Total',
            field=models.PositiveIntegerField(),
        ),
    ]
