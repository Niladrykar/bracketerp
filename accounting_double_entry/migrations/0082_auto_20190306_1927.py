# Generated by Django 2.0.6 on 2019-03-06 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_double_entry', '0081_pl_journal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pl_journal',
            name='By',
        ),
        migrations.RemoveField(
            model_name='pl_journal',
            name='Company',
        ),
        migrations.RemoveField(
            model_name='pl_journal',
            name='To',
        ),
        migrations.RemoveField(
            model_name='pl_journal',
            name='User',
        ),
        migrations.DeleteModel(
            name='pl_journal',
        ),
    ]
