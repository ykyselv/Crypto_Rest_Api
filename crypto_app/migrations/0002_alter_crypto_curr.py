# Generated by Django 4.0.3 on 2022-04-17 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('crypto_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='curr',
            field=models.CharField(choices=[('E', 'Euro'), ('D', 'Dollars'), ('R', 'Rubles')], default='R',
                                   max_length=1),
        ),
    ]
