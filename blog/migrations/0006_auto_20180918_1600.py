# Generated by Django 2.0.6 on 2018-09-18 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180918_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='Category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Categories', to='blog.categories'),
            preserve_default=False,
        ),
    ]
