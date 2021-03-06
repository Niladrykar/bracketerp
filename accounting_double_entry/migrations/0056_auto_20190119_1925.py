# Generated by Django 2.0.6 on 2019-01-19 13:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0016_auto_20190103_1923'),
        ('accounting_double_entry', '0055_contra_particularscontra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Multijournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(default=datetime.date.today)),
                ('reference', models.CharField(choices=[('To', 'To'), ('By', 'By')], default='By', max_length=32)),
                ('Debit', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('Credit', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('narration', models.TextField(blank=True)),
                ('By', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Debitledgersmulti', to='accounting_double_entry.ledger1')),
                ('Company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Companynamemultijournal', to='company.company')),
                ('To', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Creditledgersmulti', to='accounting_double_entry.ledger1')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Multijournaltotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Total_Debit', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('Total_Credit', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('Company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Companynamemultijournaltotal', to='company.company')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='multijournal',
            name='total',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='totals', to='accounting_double_entry.Multijournaltotal'),
        ),
    ]
