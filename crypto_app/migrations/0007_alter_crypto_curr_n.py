# Generated by Django 4.0.3 on 2022-04-17 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_app', '0006_alter_crypto_curr_n'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='curr_n',
            field=models.CharField(choices=[('E', 'Euro'), ('D', 'Dollars'), ('R', 'Rubles')], default='R', max_length=1),
        ),
    ]
