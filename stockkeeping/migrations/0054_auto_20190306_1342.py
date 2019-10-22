# Generated by Django 2.0.6 on 2019-03-06 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockkeeping', '0053_auto_20190305_1929'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='Total_Purchase',
            new_name='sub_total',
        ),
        migrations.RenameField(
            model_name='sales',
            old_name='Total_Amount',
            new_name='sub_total',
        ),
        migrations.RemoveField(
            model_name='stock_total_sales',
            name='cgst_total',
        ),
        migrations.RemoveField(
            model_name='stock_total_sales',
            name='gst_total',
        ),
        migrations.AddField(
            model_name='purchase',
            name='Total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='cgst_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='gst_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='Total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='cgst_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='gst_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]