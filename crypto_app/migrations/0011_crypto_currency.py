# Generated by Django 4.0.3 on 2022-04-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('crypto_app', '0010_remove_crypto_curr_n'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='currency',
            field=models.CharField(choices=[('EUR', 'Euro'), ('USD', 'Dollars'), ('UAH', 'Hryvna'), ('RUB', 'Rubbles')],
                                   default='UAH', max_length=3),
        ),
    ]
