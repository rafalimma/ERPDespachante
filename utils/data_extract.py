# utilizando ORM do Django para fazer consultas agregadas
# para a criação dos graficos e dashs.
from django.db.models import Count
from datetime import datetime
from OS.models import OrdemServico
from clientes.models import Cliente
# O Django usa essa sintaxe com __ (dois underscores) 
# para acessar partes da data, como o ano (data_servico__year) e o mês

ANO_ATUAL = datetime.now().year

def ordens_servico_mesais():
    os_por_mes = (
        OrdemServico.objects
        .filter(data_servico__year=ANO_ATUAL)
        .values('data_servico__month')
        .annotate(order_count=Count('id'))
        .order_by('data_servico__month')
    )

    meses = [os['data_servico__month'] for os in os_por_mes]
    quantidade_ordens = [os['order_count'] for os in os_por_mes]

    return meses, quantidade_ordens

def clientes_mensais():
    clientes_por_mes = (
        Cliente.objects
        .filter(data_criacao__year=ANO_ATUAL)
        .values('data_criacao__month')
        .annotate(cliente_count=Count('id'))
        .order_by('data_criacao__month')
    )

    meses = [clientes['data_criacao__month'] for clientes in clientes_por_mes]
    quantidade_clientes = [clientes['cliente_count'] for clientes in clientes_por_mes]

    return meses, quantidade_clientes