# Generated by Django 3.1.4 on 2021-01-03 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0005_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='data',
            new_name='date',
        ),
    ]
