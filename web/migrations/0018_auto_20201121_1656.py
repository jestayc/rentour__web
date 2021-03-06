# Generated by Django 3.0.4 on 2020-11-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0017_auto_20201121_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleservicio',
            name='conductor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre Conductor'),
        ),
        migrations.AlterField(
            model_name='detalleservicio',
            name='ubicacion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ubicación'),
        ),
        migrations.AlterField(
            model_name='detalleservicio',
            name='valor',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='detalleservicio',
            name='vehiculo',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Patente'),
        ),
    ]
