# Generated by Django 3.0.4 on 2020-11-21 19:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_remove_detalleservicio_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleservicio',
            name='fecha_dia',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
    ]
