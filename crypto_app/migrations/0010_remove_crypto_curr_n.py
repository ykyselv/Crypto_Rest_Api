# Generated by Django 4.0.3 on 2022-04-17 13:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('crypto_app', '0009_alter_crypto_curr_n'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crypto',
            name='curr_n',
        ),
    ]
