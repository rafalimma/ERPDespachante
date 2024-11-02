
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from OS.models import Servico
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def servicos(request):
    return paginacao(request)

@login_required
def paginacao(request):
    servicos = Servico.objects.all().values('id', 'nome', 'valor_liquido', 'valor_total')
    servicos_paginados = Paginator(servicos, 15)
    page_num = request.GET.get('page')
    servicos = servicos_paginados.get_page(page_num)

    return render(request, 'servicos.html', {'servicos': servicos})

@login_required
def editar_servico(request, id):
    servico = get_object_or_404(Servico, pk=id)
    return render(request, 'editar_servicos.html',
        {'servico': servico})

@login_required
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
        servico.nome = request.POST.get('nome')

        if servico.nome == '' or servico.valor_liquido == '':
            messages.error(request, 'Os dados não podem ser nulos!')
            return redirect(f"editar_servico/{servico_id}")
        
        servico.save()
        messages.success(request, 'Serviço alterado com sucesso!')
        return redirect('servicos')
    else:
        messages.error(request, 'Ocorreu um erro!')
        return redirect('servicos')
    
@login_required
def novo_servico(request):
    return render(request, 'novo_servico.html')

@login_required
def adicao_servico(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        custo = request.POST.get('custo')
        valor_liquido = request.POST.get('valor_liquido')
        valor_total = request.POST.get('valor_total')
        taxa_detran = request.POST.get('taxa_detran')
        notas = request.POST.get('notas')
        nome = request.POST.get('nome')

        servico = Servico(nome=nome, descricao=descricao, custo=custo,
                          valor_liquido=valor_liquido, valor_total=valor_total,
                          taxa_detran=taxa_detran, notas=notas)
        if not all([nome, descricao, custo, valor_liquido, valor_total]):
            messages.error(request, 'É necessário preencher todos os campos!')
            form_data = request.POST
            return render(request, 'novo_servico.html', {'form_data': form_data})
        else:
            servico.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
    return paginacao(request)

@login_required
def excluir_servico(request, id):
    if request.method == 'POST':
        print('excluido servico')
        servico_excluido = get_object_or_404(Servico, id=id)
        servico_excluido.delete()
        messages.success(request, "Serviço excluido com sucesso!")
        return redirect(reverse('servicos'))
    else:
        messages.error(request, "Serviço não deletado")
        return redirect(reverse('servicos'))