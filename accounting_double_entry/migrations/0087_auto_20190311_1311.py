# Generated by Django 2.0.6 on 2019-03-11 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_double_entry', '0086_auto_20190311_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pl_journal',
            old_name='credit',
            new_name='Credit',
        ),
        migrations.RenameField(
            model_name='pl_journal',
            old_name='debit',
            new_name='Debit',
        ),
    ]