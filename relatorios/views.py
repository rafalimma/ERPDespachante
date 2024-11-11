from django.shortcuts import render
import plotly.graph_objs as go # type: ignore 
from utils.data_extract import ordens_servico_mesais, clientes_mensais
# Create your views here.

def relatorios(request):
    os_por_mes = os_mensal()
    clientes_por_mes = clientes_mesal()
    return render(request, 'relatorios.html',
                {'os_por_mes': os_por_mes,
                 'clientes_por_mes': clientes_por_mes})

def os_mensal():
    meses, os_qtds = ordens_servico_mesais()
    fig = go.Figure(data=go.Scatter(
        x=meses,
         y=os_qtds,
        mode='lines+markers',
        line=dict(color='#f27e34')
        ))
    fig.update_layout(
        # title='Ordens de Serviço por Mês',
        xaxis_title='Mês',
        yaxis_title='Número de Ordens',
        xaxis=dict(showgrid=False,
                   tickmode='array',# Define os valores como uma lista de categorias
                   tickvals=meses,
            ),
        yaxis=dict(showgrid=False),
        plot_bgcolor='#85d794',
        margin=dict(l=0, r=0, t=20, b=20)
    )
    config = {
        'displayModeBar': False,  # Remove a barra de ferramentas
        'staticPlot': True        # Desativa o modo interativo
    }

    grafico_html = fig.to_html(full_html=False, config=config)
    return grafico_html

def clientes_mesal():
    meses, clientes_qtd = clientes_mensais()
    fig = go.Figure(data=go.Scatter(
        x=meses,
         y=clientes_qtd,
        mode='lines+markers',
        line=dict(color='#f27e34')
        ))
    fig.update_layout(
        # title='Ordens de Serviço por Mês',
        xaxis_title='Mês',
        yaxis_title='Clientes',
        xaxis=dict(showgrid=False,
                   tickmode='array',# Define os valores como uma lista de categorias
                   tickvals=meses,
            ),
        yaxis=dict(showgrid=False),
        plot_bgcolor='#85d794',
        margin=dict(l=0, r=0, t=20, b=20)
    )
    config = {
        'displayModeBar': False,  # Remove a barra de ferramentas
        'staticPlot': True        # Desativa o modo interativo
    }

    grafico_html = fig.to_html(full_html=False, config=config)
    return grafico_html
