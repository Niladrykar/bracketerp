# Generated by Django 2.0.6 on 2019-03-16 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0031_organisation_member_member_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='qualification',
            field=models.CharField(blank=True, choices=[('Pending for verification', 'Pending for verification'), ('Verified', 'Verified')], default='Pending for verification', max_length=100),
        ),
    ]
