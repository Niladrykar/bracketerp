# Generated by Django 2.0.6 on 2019-02-02 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_double_entry', '0064_auto_20190125_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='particularscontra',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]