# Generated by Django 2.0.6 on 2018-09-19 07:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20180915_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]