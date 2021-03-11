# Generated by Django 3.1.2 on 2020-11-06 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_departamento_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleservicio',
            name='conductor',
            field=models.CharField(max_length=100, null=True, verbose_name='Nombre Conductor'),
        ),
        migrations.AlterField(
            model_name='detalleservicio',
            name='id_tiposervicioextra',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.tiposervicioextra'),
        ),
        migrations.AlterField(
            model_name='detalleservicio',
            name='ubicacion',
            field=models.CharField(max_length=100, null=True, verbose_name='Ubicación'),
        ),
        migrations.AlterField(
            model_name='detalleservicio',
            name='vehiculo',
            field=models.CharField(max_length=10, null=True, verbose_name='Patente'),
        ),
    ]