# Generated by Django 5.0 on 2024-05-22 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OS', '0016_remove_ordemservico_servico_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordemservico',
            name='cpf_cnpj',
        ),
    ]