# Generated by Django 3.1.4 on 2021-05-01 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0015_portfolio_portolio_return'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolio',
            old_name='portolio_return',
            new_name='portfolio_return',
        ),
    ]
