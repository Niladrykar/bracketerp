# Generated by Django 2.0.6 on 2018-09-28 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_double_entry', '0004_group1_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group1',
            name='Company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Company_group', to='company.company'),
        ),
    ]
