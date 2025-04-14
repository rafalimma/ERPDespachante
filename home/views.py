from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from relatorios import views as relatorioviews
from OS.models import OrdemServico
from datetime import datetime, timedelta
# Create your views here.
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
@login_required
def home(request):
    hoje = datetime.now()
    menostrinta = hoje - timedelta(days=30)
    menosquanze = hoje - timedelta(days=15)
    periodo = request.GET.get('periodo')
    os_grafico = relatorioviews.os_grafico_calculo(periodo)
    clientes_grafico = relatorioviews.clientes_grafico_calculo(periodo)
    if not periodo == 'dias':
        os_pendentes = OrdemServico.objects.filter(status="pendente").count()
        os_faturadas = OrdemServico.objects.filter(status="Servico Faturado").count()
    else:
        os_pendentes = OrdemServico.objects.filter(status="pendente", data_servico__gte=menosquanze).count()
        os_faturadas = OrdemServico.objects.filter(status="Servico Faturado", data_servico__gte=menosquanze).count()
    
    

    return render(
        request,
        'home.html',
        {'os_grafico': os_grafico,
        'clientes_grafico': clientes_grafico,
        'periodo': periodo,
        "os_pendentes": os_pendentes,
        "os_faturadas": os_faturadas}
    )

def voltar(request):
    if 'url_stack' in request.session:
        url_stack = request.session['url_stack']

        if len(url_stack) > 1:
            # Remove a URL atual e retorna para a anterior
            url_stack.pop()  # Remove a URL atual
            request.session['url_stack'] = url_stack
            print(f"Redirecionando para {url_stack[-1]}")
            if url_stack[-2] == '/home/':
                url_stack[-2] = '/home/?periodo=mensal'
            return redirect(url_stack[-2])
    return redirect('/')