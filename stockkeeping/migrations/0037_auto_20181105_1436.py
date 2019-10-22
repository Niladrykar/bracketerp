# Generated by Django 2.0.6 on 2018-11-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockkeeping', '0036_auto_20181105_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockdata',
            name='Total_SP',
        ),
        migrations.AddField(
            model_name='stockdata',
            name='Total_PS',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]