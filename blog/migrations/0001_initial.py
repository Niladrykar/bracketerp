# Generated by Django 2.0.6 on 2018-09-15 11:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateTimeField(default=datetime.datetime.now)),
                ('Blog_title', models.CharField(max_length=32)),
                ('Description', models.TextField(blank=True, max_length=255)),
                ('Blog_image', models.ImageField(blank=True, null=True, upload_to='blog_image')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
