# Generated by Django 3.1.4 on 2021-01-03 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0007_transactiontwo'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='cash',
            field=models.FloatField(default=1000000),
        ),
    ]
