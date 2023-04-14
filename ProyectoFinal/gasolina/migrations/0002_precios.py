# Generated by Django 4.1.5 on 2023-04-04 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gasolina', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Precios',
            fields=[
                ('id_precio', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_gasolina', models.CharField(max_length=45, verbose_name='Tipo Gasolina')),
                ('precio', models.IntegerField(verbose_name='Precio Gasolina')),
                ('fk_id_gasolineria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gasolina.gasolinerias')),
            ],
        ),
    ]