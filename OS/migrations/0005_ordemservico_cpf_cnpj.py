# Generated by Django 5.0 on 2024-04-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OS', '0004_remove_ordemservico_cpf_cnpj'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemservico',
            name='cpf_cnpj',
            field=models.CharField(default='', max_length=14),
        ),
    ]
