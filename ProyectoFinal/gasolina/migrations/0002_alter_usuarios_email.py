# Generated by Django 4.1.5 on 2023-04-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gasolina', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
    ]
