# Generated by Django 5.2.3 on 2025-06-13 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asamblea', '0002_puesto_num_curul_alter_lista_name_alter_plancha_fc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puesto',
            name='num_curul',
            field=models.IntegerField(choices=[(7, '7'), (8, '8'), (13, '13'), (14, '14'), (17, '17')], default=0, verbose_name='¿N° Curules?'),
        ),
    ]
