# Generated by Django 3.1.4 on 2021-01-01 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('ticker', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('compnay', models.CharField(max_length=100)),
            ],
        ),
    ]