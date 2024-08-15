
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from OS.models import Servico

# Create your views here.

def servicos(request):
    return paginacao(request)

def paginacao(request):
    servicos = Servico.objects.all().values('id', 'descricao', 'valor_liquido', 'valor_total')
    servicos_paginados = Paginator(servicos, 10)
    page_num = request.GET.get('page')
    servicos = servicos_paginados.get_page(page_num)

    return render(request, 'servicos.html', {'servicos': servicos})

def editar_servico(request, id):
    servico = get_object_or_404(Servico, pk=id)
    return render(request, 'editar_servicos.html',
        {'servico': servico})

def form_edicao_servico(request):
    if request.method == 'POST':
        servico_id = request.POST.get('id_servico')
        servico = get_object_or_404(Servico, pk=servico_id)
        servico.descricao = request.POST.get('descricao')
        servico.custo = request.POST.get('custo')
        servico.valor_liquido = request.POST.get('valor_liquido')
        servico.taxa_detran = request.POST.get('taxa_detran')
        servico.valor_total = request.POST.get('valor_total')
        servico.notas = request.POST.get('notas')

        servico.save()
        messages.success(request, 'Serviço alterado com sucesso!')
        return redirect('servicos')
    else:
        messages.error(request, 'Ocorreu um erro!')
        return redirect('servicos')
    
def novo_servico(request):
    return render(request, 'novo_servico.html')

def adicao_servico(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        custo = request.POST.get('custo')
        valor_liquido = request.POST.get('valor_liquido')
        valor_total = request.POST.get('valor_total')
        taxa_detran = request.POST.get('taxa_detran')
        notas = request.POST.get('notas')

        servico = Servico(descricao=descricao, custo=custo,
                          valor_liquido=valor_liquido, valor_total=valor_total,
                          taxa_detran=taxa_detran, notas=notas)
        if not all([descricao, custo, valor_liquido, valor_total]):
            messages.error(request, 'É necessário preencher todos os campos!')
            return redirect(reverse('novo_servico'))
        else:
            servico.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
    return paginacao(request)