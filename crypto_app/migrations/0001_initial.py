# Generated by Django 4.0.3 on 2022-04-08 19:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('cp_curr', models.CharField(max_length=255)),
                ('curr', models.CharField(max_length=255)),
                ('price', models.FloatField()),
            ],
        ),
    ]
