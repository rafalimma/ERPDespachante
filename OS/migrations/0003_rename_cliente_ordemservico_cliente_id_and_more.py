# Generated by Django 5.0 on 2024-04-21 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OS', '0002_alter_ordemservico_processo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordemservico',
            old_name='cliente',
            new_name='cliente_id',
        ),
        migrations.RenameField(
            model_name='ordemservico',
            old_name='name',
            new_name='nome_cliente',
        ),
    ]
