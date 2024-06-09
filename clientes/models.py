from django.db import models

# Create your models here.
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
#models do cadastro de clientes:

class Cliente(models.Model):
    name = models.CharField(max_length=40)
    cpf_cnpj = models.CharField(max_length=14)
    telefone = models.CharField(max_length=11)
    cep = models.CharField(max_length=50, default='')
    bairro = models.CharField(max_length=30, default='')
    cidade = models.CharField(max_length=15, default='')
    numero = models.CharField(max_length=6, default='')
