# Generated by Django 5.0 on 2024-05-17 00:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OS', '0013_alter_ordemservico_pendencias'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servico_os',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OS.ordemservico')),
                ('servico_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OS.servico')),
            ],
        ),
    ]