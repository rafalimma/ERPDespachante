# Generated by Django 5.0 on 2024-05-19 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OS', '0014_servico_os'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordemservico',
            name='processo',
        ),
        migrations.AddField(
            model_name='servico_os',
            name='valor_servico',
            field=models.CharField(default='', max_length=10),
        ),
    ]
