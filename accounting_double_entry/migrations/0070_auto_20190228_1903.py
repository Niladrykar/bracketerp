# Generated by Django 2.0.6 on 2019-02-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_double_entry', '0069_auto_20190228_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group1',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]