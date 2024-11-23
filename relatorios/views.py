from django.shortcuts import render
import plotly.graph_objs as go # type: ignore 
from utils.data_extract import ordens_servico_mesais, clientes_mensais
from utils.data_extract import ordens_servico_diarias, clientes_diarios
from clientes.models import Cliente
from OS.models import OrdemServico, Servico
from django.db.models import Max
from django.core.cache import cache
from relatorios.models import Relatorios
from datetime import datetime
from django.utils.timezone import make_aware
from django.http import JsonResponse
# Create your views here.

NOME_MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
def relatorios(request):
    periodo = request.GET.get('periodo')
    os_grafico = os_grafico_calculo(periodo)
    clientes_grafico = clientes_grafico_calculo(periodo)
    # a variavel periodo indica qual o periodo do grafico gerado e também
    # é retornado para o template para definir o botão ativo
    return render(request, 'relatorios.html',
                {'os_grafico': os_grafico,
                 'clientes_grafico': clientes_grafico,
                 'periodo': periodo})

# função que retorna as datas dos ultimos objetos para o cache
def ultima_criacao():
    ultimo_objeto_cliente = Cliente.objects.aggregate(Max('data_criacao'))['data_criacao__max']
    ultimo_objeto_ordem = OrdemServico.objects.aggregate(Max('data_servico'))['data_servico__max']
    return ultimo_objeto_cliente, ultimo_objeto_ordem

def os_grafico_calculo(periodo):
    # data_ultima_criacao = ultima_criacao()
    # # tem que melhorar essa key chace pois pode dar problemas
    # cache_key = f"os_mensal{data_ultima_criacao}"
    # grafico_html = cache.get(cache_key)
    if periodo == 'mensal':
        try:
            data_ultimo_relatorio = Relatorios.objects.filter(tipo="ordem de serviço por mês").latest('data_atualizacao')
            data_ultima_os = OrdemServico.objects.latest('data_servico')
            # convertendo para DateTime
            data_ultima_os_datetime = make_aware(datetime.combine(data_ultima_os.data_servico, datetime.min.time()))
            print('data da ultima os: ', data_ultima_os_datetime)
            if data_ultima_os_datetime > data_ultimo_relatorio.data_atualizacao:
                meses, os_qtds = ordens_servico_mesais()
            else:
                meses = data_ultimo_relatorio.get_meses()
                os_qtds = data_ultimo_relatorio.get_quantidade()
        except Relatorios.DoesNotExist:
            meses, os_qtds = ordens_servico_mesais()
        meses = [NOME_MESES[int(m) - 1] for m in meses]

        fig = go.Figure(data=go.Scatter(
            x=meses,
            y=os_qtds,
            mode='lines+markers+text',
            line=dict(color='#00bf63'),
            fill='tozeroy',
            fillcolor='#6ce093',
            text=os_qtds,
            textfont=dict(size=12, color='black'),
            textposition='top center',
            showlegend=False,
        ))
                
        fig.update_layout(
            # title='Ordens de Serviço por Mês',
            width=490,
            height=300,
            yaxis_title='Número de Ordens',
            xaxis=dict(showgrid=False,
                    range=[-0.1, len(meses) - 0.9],
                    tickmode='array',# Define os valores como uma lista de categorias
                    tickvals=list(range(len(meses))),
                    ticktext=meses,
                    zeroline=False,
                ),
            yaxis=dict(showgrid=False,
                    zeroline=False,
                ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=20),
        )
        config = {
            'displayModeBar': False,  # Remove a barra de ferramentas
            'staticPlot': True,        # Desativa o modo interativo
        }

        grafico_html = fig.to_html(full_html=False, config=config)
        return grafico_html
    elif periodo == "dias":
        dias, os_qtds = ordens_servico_diarias()

        fig = go.Figure(data=go.Scatter(
            x=dias,
            y=os_qtds,
            mode='lines+markers+text',
            line=dict(color='#00bf63'),
            fill='tozeroy',
            fillcolor='#6ce093',
            text=os_qtds,
            textfont=dict(size=12, color='black'),
            textposition='top center',
            showlegend=False,
        ))

        fig.update_layout(
            # title='Ordens de Serviço por Mês',
            width=490,
            height=300,
            yaxis_title='Número de Ordens',
            xaxis=dict(showgrid=False,
                    range=[-0.1, len(dias) - 0.9],
                    tickmode='array',# Define os valores como uma lista de categorias
                    tickvals=list(range(len(dias))),
                    zeroline=False,
                ),
            yaxis=dict(showgrid=False,
                    zeroline=False,
                ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=20),
        )

        config = {
            'displayModeBar': False,  # Remove a barra de ferramentas
            'staticPlot': True,        # Desativa o modo interativo
        }
        grafico_html = fig.to_html(full_html=False, config=config)
        return grafico_html


def clientes_grafico_calculo(periodo):
    if periodo == "mensal":
        try:
            data_ultimo_relatorio = Relatorios.objects.filter(tipo="clientes por mês").latest('data_atualizacao')
            data_ultimo_cliente = Cliente.objects.latest('data_criacao')
            if data_ultimo_cliente.data_criacao > data_ultimo_relatorio.data_atualizacao:
                meses, clientes_qtd = clientes_mensais()
            else:
                meses = data_ultimo_relatorio.get_meses()
                clientes_qtd = data_ultimo_relatorio.get_quantidade()
        except:
            print('criando primeiro registro do relatório')
            meses, clientes_qtd = clientes_mensais()
        meses = [NOME_MESES[int(m) - 1]for m in meses]
        fig = go.Figure(data=go.Scatter(
            x=meses,
            y=clientes_qtd,
            mode='lines+markers+text',
            line=dict(color='#00bf63'),
            fill='tozeroy',
            fillcolor='#6ce093',
            text=clientes_qtd,
            textposition='top center'
            ))
        fig.update_layout(
            width=490,
            height=300,
            yaxis_title='Clientes',
            xaxis=dict(showgrid=False,
                    tickmode='array',# Define os valores como uma lista de categorias
                    tickvals=list(range(len(meses))),
                    range=[-0.1, len(meses) - 0.9],
                    ticktext=meses,
                    zeroline=False,
                ),
            yaxis=dict(showgrid=False,
                    zeroline=False,
                    ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=20)
        )
        config = {
            'displayModeBar': False,  # Remove a barra de ferramentas
            'staticPlot': True        # Desativa o modo interativo
        }

        grafico_html = fig.to_html(full_html=False, config=config)
        return grafico_html
    elif periodo == "dias":
        dias, clientes_qtd = clientes_diarios()

        fig = go.Figure(data=go.Scatter(
            x=dias,
            y=clientes_qtd,
            mode='lines+markers+text',
            line=dict(color='#00bf63'),
            fill='tozeroy',
            fillcolor='#6ce093',
            text=clientes_qtd,
            textfont=dict(size=12, color='black'),
            textposition='top center',
            showlegend=False,
        ))

        fig.update_layout(
            # title='Ordens de Serviço por Mês',
            width=490,
            height=300,
            yaxis_title='Número de Ordens',
            xaxis=dict(showgrid=False,
                    range=[-0.1, len(dias) - 0.9],
                    tickmode='array',# Define os valores como uma lista de categorias
                    tickvals=list(range(len(dias))),
                    zeroline=False,
                ),
            yaxis=dict(showgrid=False,
                    zeroline=False,
                ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=20),
        )

        config = {
            'displayModeBar': False,  # Remove a barra de ferramentas
            'staticPlot': True,        # Desativa o modo interativo
        }
        grafico_html = fig.to_html(full_html=False, config=config)
        return grafico_html
