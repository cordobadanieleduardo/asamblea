# Generated by Django 5.2.3 on 2025-06-19 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asamblea', '0009_alter_puesto_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puesto',
            name='fecha_fin',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha cierre'),
        ),
        migrations.AlterField(
            model_name='puesto',
            name='fecha_inicio',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de inicio'),
        ),
    ]
