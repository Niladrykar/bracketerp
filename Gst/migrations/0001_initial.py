# Generated by Django 2.0.6 on 2019-03-05 08:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0019_company_urlhash'),
        ('stockkeeping', '0050_auto_20190302_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gst_input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('gstin_vendor', models.CharField(default='19ABCDE1234F2Z5', max_length=100, unique=True)),
                ('gstin_self', models.CharField(default='19ABCDE1234F2Z5', max_length=100, unique=True)),
                ('cgst', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('sgst', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('igst', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('ugst', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('withinstate', models.BooleanField(default=False)),
                ('Company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Company_gstinput', to='company.company')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Purchasegst', to='stockkeeping.Purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Gst_output',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('gstin_vendor', models.CharField(default='19ABCDE1234F2Z5', max_length=100, unique=True)),
                ('gstin_self', models.CharField(default='19ABCDE1234F2Z5', max_length=100, unique=True)),
                ('cgst', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('sgst', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('igst', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('ugst', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('withinstate', models.BooleanField(default=False)),
                ('Company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Company_gstoutput', to='company.company')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salesgst', to='stockkeeping.Sales')),
            ],
        ),
    ]
