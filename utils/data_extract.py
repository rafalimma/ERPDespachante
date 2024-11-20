# utilizando ORM do Django para fazer consultas agregadas
# para a criação dos graficos e dashs.
from django.db.models import Count
from datetime import datetime
from OS.models import OrdemServico
from clientes.models import Cliente
from relatorios.models import Relatorios
from django.db import transaction
# O Django usa essa sintaxe com __ (dois underscores) 
# para acessar partes da data, como o ano (data_servico__year) e o mês

ANO_ATUAL = datetime.now().year

def ordens_servico_mesais():
    print('passando por servicos')
    os_por_mes = (
        OrdemServico.objects
        .filter(data_servico__year=ANO_ATUAL)
        .values('data_servico__month')
        .annotate(order_count=Count('id'))
        .order_by('data_servico__month')
    )

    meses = [os['data_servico__month'] for os in os_por_mes]
    quantidade_ordens = [os['order_count'] for os in os_por_mes]

    with transaction.atomic(): # define que esse bloco de codigo seja atomico para o banco de dados, 
        # se alguma parte falhar todas as alterações no banco feitas por esse bloco de código serão revertidas
        Relatorios.objects.filter(tipo="ordem se serviço por mês").delete()

        relatorio_atual = Relatorios(tipo="ordem de serviço por mês")
        relatorio_atual.set_meses(meses)
        relatorio_atual.set_quantidade(quantidade_ordens)
        relatorio_atual.save()
    
    return meses, quantidade_ordens

def clientes_mensais():
    print('passando por clientes')
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