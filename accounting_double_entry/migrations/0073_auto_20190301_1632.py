# Generated by Django 2.0.6 on 2019-03-01 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_double_entry', '0072_group1_group_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group1',
            name='urlhash',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
