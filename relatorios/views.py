from django.shortcuts import render
import plotly.graph_objs as go # type: ignore 
from utils.data_extract import ordens_servico_mesais, clientes_mensais
# Create your views here.

NOME_MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
def relatorios(request):
    os_por_mes = os_mensal()
    clientes_por_mes = clientes_mesal()
    return render(request, 'relatorios.html',
                {'os_por_mes': os_por_mes,
                 'clientes_por_mes': clientes_por_mes})

# tons de laranja: #ecaa86,  #f27e34

def os_mensal():
    meses, os_qtds = ordens_servico_mesais()
    meses = [NOME_MESES[m - 1]for m in meses]
    fig = go.Figure(data=go.Scatter(
        x=meses,
        y=os_qtds,
        mode='lines+markers+text',
        line=dict(color='#00bf63'),
        fill='tozeroy',
        fillcolor='#6ce093',
        text=os_qtds,
        textfont=dict(size=12, color='black'),
        textposition='bottom center',
        showlegend=False,
        ))
    fig.update_layout(
        # title='Ordens de Serviço por Mês',
        width=490,
        height=300,
        yaxis_title='Número de Ordens',
        xaxis=dict(showgrid=False,
                   tickmode='array',# Define os valores como uma lista de categorias
                   tickvals=meses,
            ),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=20),
    )
    config = {
        'displayModeBar': False,  # Remove a barra de ferramentas
        'staticPlot': True        # Desativa o modo interativo
    }

    grafico_html = fig.to_html(full_html=False, config=config)
    return grafico_html

def clientes_mesal():
    meses, clientes_qtd = clientes_mensais()
    meses = [NOME_MESES[m - 1]for m in meses]
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
                   tickvals=meses,
            ),
        yaxis=dict(showgrid=False),
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
