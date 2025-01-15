from django.db import models
from OS.models import OrdemServico
import datetime
# Create your models here.

class Fatura(models.Model):
    os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="")
    forma_pagamento = models.CharField(max_length=50, default="")
    data_vencimento = models.DateField(null=True, blank=True)
    solicitante = models.CharField(max_length=100, default="")
    tomador = models.CharField(max_length=100, default="")
    n_parcelas = models.IntegerField(default=1)
    valor_final = models.CharField(max_length=50)
    custo_final = models.CharField(max_length=50)
    arrecadacao_final = models.CharField(max_length=50)
    lucro_total = models.CharField(max_length=50, default="")

class Parcela(models.Model):
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE)
    numeracao = models.IntegerField(default=0)
    valor_parcela = models.CharField(max_length=20, default="")
    status = models.CharField(max_length=20, default="")

class EventoFatura(models.Model):
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE)
    status_anterior = models.CharField(max_length=30, default='')
    status_atual = models.CharField(max_length=30, default='')
    observacoes = models.TextField(blank=True, null=True)
    data = models.DateField(default=datetime.date.today)
    horario = models.TimeField(auto_now_add=True)

