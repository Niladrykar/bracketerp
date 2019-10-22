# Generated by Django 2.0.6 on 2018-11-03 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockkeeping', '0026_remove_stock_total_total_sales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock_Total_sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.PositiveIntegerField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Disc', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('gst_rate', models.DecimalField(decimal_places=2, default=5, max_digits=4)),
                ('Total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='Total_Amount',
            new_name='Total_Purchase',
        ),
        migrations.RemoveField(
            model_name='stock_total',
            name='sales',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='Contact',
            field=models.BigIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sales',
            name='Contact',
            field=models.BigIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saleledger', to='accounting_double_entry.ledger1'),
        ),
        migrations.AddField(
            model_name='stock_total_sales',
            name='sales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saletotal', to='stockkeeping.Sales'),
        ),
        migrations.AddField(
            model_name='stock_total_sales',
            name='stockitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salestock', to='stockkeeping.Stockdata'),
        ),
    ]