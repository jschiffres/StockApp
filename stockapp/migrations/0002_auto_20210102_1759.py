# Generated by Django 3.1.4 on 2021-01-02 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='compnay',
            new_name='company',
        ),
    ]