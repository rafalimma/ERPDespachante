from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from relatorios import views as relatorioviews
# Create your views here.
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
@login_required
def home(request):
    print('passou pela home')
    periodo = request.GET.get('periodo')
    os_grafico = relatorioviews.os_grafico_calculo(periodo)
    clientes_grafico = relatorioviews.clientes_grafico_calculo(periodo)
    return render(
        request,
        'home.html',
        {'os_grafico': os_grafico,
        'clientes_grafico': clientes_grafico,
        'periodo': periodo}
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