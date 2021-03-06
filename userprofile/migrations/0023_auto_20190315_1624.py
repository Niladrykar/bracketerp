# Generated by Django 2.0.6 on 2019-03-15 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0022_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pro_services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(blank=True, max_length=100)),
                ('details', models.CharField(blank=True, max_length=100)),
                ('service_type', models.CharField(blank=True, choices=[('Returns', 'Returns'), ('Communication', 'Communication'), ('License', 'License')], default='Returns', max_length=100)),
                ('duration', models.CharField(blank=True, choices=[('ANNUALLY', 'ANNUALLY'), ('QUARTERLY', 'QUARTERLY'), ('ONE TIME', 'ONE TIME')], default='ANNUALLY', max_length=100)),
                ('service_mode', models.CharField(blank=True, choices=[('ON-PREMISES', 'ON-PREMISES'), ('CALLS - VOIP', 'CALLS - VOIP'), ('COLLECTION FROM CLIENT', 'COLLECTION FROM CLIENT')], default='ON-PREMISES', max_length=100)),
                ('rate', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='services',
            name='User',
        ),
        migrations.DeleteModel(
            name='Services',
        ),
    ]
