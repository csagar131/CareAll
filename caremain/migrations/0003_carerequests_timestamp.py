# Generated by Django 2.2.10 on 2020-05-27 18:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('caremain', '0002_auto_20200523_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='carerequests',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
