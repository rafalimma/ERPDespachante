from django.shortcuts import render, get_object_or_404, redirect
from .models import Fatura
from OS.models import OrdemServico
# Create your views here.

def faturamento(request):
    return render(request, 'faturamento.html')

def criar_fatura(id_os):
    os = OrdemServico.objects.get(pk=id_os)
    fatura = Fatura(os=os, status="aberto", forma_pagamento="",
                    data_vencimento=None, solicitante=os.nome_cliente,
                    tomador=None, n_parcelas=None, valor_final=os.valor_f,
                    custo_final=None, arrecadacao_final=None, lucro_total=None)
    fatura.save()