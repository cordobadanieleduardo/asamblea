# Generated by Django 5.2.1 on 2025-05-29 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asamblea', '0003_militante_must_change_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='militante',
            name='change_password',
        ),
    ]
