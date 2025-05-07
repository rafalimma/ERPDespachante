from django.db import models
from OS.models import OrdemServico
from clientes.models import Cliente
import datetime
# Create your models here.

class Fatura(models.Model):
    os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="") # cancelada, pendente, parcial, pago
    forma_pagamento = models.CharField(max_length=50, default="", null=True)
    data_vencimento = models.DateField(null=True, blank=True)
    solicitante = models.CharField(max_length=100, default="")
    tomador = models.CharField(max_length=100, default="", null=True)
    n_parcelas = models.IntegerField(default=1, null=True)
    valor_final = models.CharField(max_length=50)
    lucro_total = models.CharField(max_length=50, default="", null=True)

class Pagamento(models.Model):
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE)
    valor_pago = models.CharField(max_length=20, default="")
    forma_pagamento = models.CharField(max_length=30, default='')
    data_pagamento = models.DateField(default=datetime.date.today)

class EventoFatura(models.Model):
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE)
    status_anterior = models.CharField(max_length=30, default='')
    status_atual = models.CharField(max_length=30, default='')
    observacoes = models.TextField(blank=True, null=True)
    data = models.DateField(default=datetime.date.today)
    horario = models.TimeField(auto_now_add=True)

