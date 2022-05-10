# Generated by Django 4.0.3 on 2022-04-17 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_app', '0004_remove_crypto_curr_n'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='curr_n',
            field=models.CharField(choices=[('E', 'Euro'), ('D', 'Dollars'), ('R', 'Rubles')], default='R', max_length=1),
        ),
    ]