from django.db import models
from datetime import date
from django.utils.timezone import now
# Create your models here.
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
#models do cadastro de clientes:

class Cliente(models.Model):
    name = models.CharField(max_length=40)
    cpf_cnpj = models.CharField(max_length=25)
    telefone = models.CharField(max_length=25)
    cep = models.CharField(max_length=50, default='')
    bairro = models.CharField(max_length=30, default='')
    estado = models.CharField(max_length=30, default='')
    cidade = models.CharField(max_length=25, default='')
    numero = models.CharField(max_length=10, default='')
    email = models.EmailField(max_length=100, null=True, blank=True)
    rua = models.CharField(max_length=100, default='')
    data_criacao = models.DateTimeField(auto_now_add=True)
