# Generated by Django 2.0.6 on 2019-02-28 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_double_entry', '0070_auto_20190228_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='group1',
            name='urlhash',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]
