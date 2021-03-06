# Generated by Django 2.0.6 on 2019-03-05 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockkeeping', '0051_auto_20190305_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock_total',
            name='gst_rate_p',
        ),
        migrations.RemoveField(
            model_name='stock_total_sales',
            name='gst_rate',
        ),
        migrations.AddField(
            model_name='stock_total',
            name='cgst',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='stock_total',
            name='igst',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='stock_total',
            name='sgst',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='stock_total',
            name='ugst',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='stock_total_sales',
            name='cgst',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='stock_total_sales',
            name='igst',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='stock_total_sales',
            name='sgst',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='stock_total_sales',
            name='ugst',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
