# Generated by Django 2.2.10 on 2020-06-27 12:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caremain', '0006_auto_20200627_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_for', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 27, 17, 53, 28, 186670)),
        ),
    ]
