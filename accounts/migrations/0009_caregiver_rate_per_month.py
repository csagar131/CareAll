# Generated by Django 2.2.10 on 2020-06-16 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='caregiver',
            name='rate_per_month',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
