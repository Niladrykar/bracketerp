# Generated by Django 2.0.6 on 2019-02-27 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0016_auto_20181027_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog_comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Questions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_comments', to='blog.Blog')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
