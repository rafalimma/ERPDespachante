# Generated by Django 5.0 on 2024-03-05 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_rename_nome_cliente_name_alter_cliente_cpf_cnpj_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='bairro',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cep',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cidade',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='cliente',
            name='numero',
            field=models.CharField(default='', max_length=6),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(max_length=11),
        ),
    ]
