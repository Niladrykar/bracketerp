# Generated by Django 2.0.6 on 2019-03-02 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_double_entry', '0078_auto_20190302_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='contra',
            name='counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contra',
            name='urlhash',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='urlhash',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='ledger1',
            name='counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ledger1',
            name='urlhash',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='urlhash',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='urlhash',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
