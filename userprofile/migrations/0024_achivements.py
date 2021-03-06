# Generated by Django 2.0.6 on 2019-03-15 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0023_auto_20190315_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='achivements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_case', models.BooleanField(default=False)),
                ('act', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('facts', models.CharField(blank=True, max_length=100)),
                ('issue', models.CharField(blank=True, max_length=100)),
                ('argument', models.CharField(blank=True, max_length=100)),
                ('judgement', models.CharField(blank=True, max_length=100)),
                ('user_role', models.CharField(blank=True, max_length=100)),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
