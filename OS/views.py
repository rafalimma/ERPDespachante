from django.shortcuts import render, get_object_or_404, redirect
from clientes.models import Cliente
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import OrdemServico, Servico, Servico_os, Documentos
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from time import strftime
from django.template.loader import get_template
from xhtml2pdf import pisa
from weasyprint import HTML
from django.template.loader import render_to_string 
from datetime import date
import weasyprint
from django.conf import settings
from django.contrib.staticfiles import finders
import tempfile
DEFAULT_DATE = ""


def teste(request):
    clientes = Cliente.objects.all()
    servicos = Servico.objects.all()
    return render(request, 'teste.html', {'clientes': clientes, 'servicos': servicos})

def ordem_servico(request):
    return paginacao(request)
    # ordens = OrdemServico.objects.all()
    # return render(request, 'os.html', {'ordens_servicos': ordens})

def newos(request):
    clientes = Cliente.objects.all()
    servicos = Servico.objects.all()
    return render(request, 'newos.html', {'clientes': clientes, 'servicos': servicos})

def nova_ordem_de_servico(request):
    if request.method == 'POST':
        print('nova 0rdem entrou')
        name = request.POST.get('name') #entre as aspas vai o name que esta no formulário
        id_cliente = request.POST.get('id_cliente')
        renavam = request.POST.get('renavam')
        placa = request.POST.get('placa')
        valor = request.POST.get('valor')
        chassi = request.POST.get('chassi')
        cor = request.POST.get('cor')
        combustivel = request.POST.get('combustivel')
        data_aq = request.POST.get('data')
        modelo = request.POST.get('modelo')
        ano_veiculo = request.POST.get('ano')
        pendencias = request.POST.get('pendencias')
        data_entrega = request.POST.get('dtentrega')
        desconto = request.POST.get('desconto')
        valor_f = request.POST.get('vfinal')
        id_servico = request.POST.get('id_servico')
        valor_servico = request.POST.get('valorservico')
        observacoes = request.POST.get('observacoes')
        status = request.POST.get('status')
        cpf_vendedor = request.POST.get('cpf_vendedor')
        concessionaria = request.POST.get('concessionaria')
        tipo_veiculo = request.POST.get('tipo_veiculo')
        servico = request.POST.get('servico')

        tipo_doc = request.POST.get('tipo_doc')
        arquivo = request.FILES.get('file')
        #verifica se outros campos de arquivos foram criados:
        if request.FILES.get('file1'):
            tipo_doc1 = request.POST.get('tipo_doc1')
            arquivo1 = request.FILES.get('file1')
            print('aqui foi file1')
        if request.FILES.get('file2'):
            print('aqui foi file2')
            tipo_doc2 = request.POST.get('tipo_doc2')
            arquivo2 = request.FILES.get('file2')
        # verifica se outros serviços foram criados:
        if request.POST.get('servico1'):
            id_servico2 = request.POST.get('id_servico1')
            valor_servico2 = request.POST.get('valorservico1')
        if request.POST.get('servico2'):
            valor_servico3 = request.POST.get('valorservico2')
            id_servico3 = request.POST.get('id_servico2')
        # faz verificações se o id do cliente e se as datas não foram preenchidas:
        if not(id_cliente):
            messages.error(request, 'É necessário preencher todos os campos! ID cliente')
            clientes = Cliente.objects.all()
            servicos = Servico.objects.all()
            # capturando os dados do formulário (requsição post passada)
            form_data = request.POST
            return render(request, 'newos.html', {
                'clientes': clientes,
                'servicos': servicos,
                'form_data': form_data
            })
        if not data_aq:
            data_aq = None
        if not data_entrega:
            data_entrega = None
        # pega a chave primária do cliente
        cliente = Cliente.objects.get(pk=id_cliente)

        ordem_de_servico = OrdemServico(
            nome_cliente=name, cliente_id=cliente, renavam=renavam,
            placa=placa, chassi=chassi,
            cor=cor, combustivel=combustivel, data_aq=data_aq,
            modelo=modelo, valor_veiculo=valor, ano_modelo=ano_veiculo,
            pendencias=pendencias, data_entrega=data_entrega,
            desconto=desconto, valor_f=valor_f, observacoes=observacoes,
            status=status, concessionaria=concessionaria, cpf_vendedor=cpf_vendedor,
            tipo_veiculo=tipo_veiculo
            )
        if not all([renavam, placa, cliente, name,
                     combustivel, modelo, ano_veiculo, id_servico, data_entrega,
                     valor_servico, valor_f, status, cpf_vendedor, tipo_veiculo]):
            messages.error(request, 'É necessário preencher todos os campos! CAMPOS')
            clientes = Cliente.objects.all()
            servicos = Servico.objects.all()
            form_data = request.POST
            print('indo pro htttp reffer')
            return render(request, 'newos.html', {
                'clientes': clientes,
                'servicos': servicos,
                'form_data': form_data
            })
        else:
            ordem_de_servico.save()
            # salva o serviço padrão
            id_servico = Servico.objects.get(pk=id_servico)
            servico_ordem_servico = Servico_os(
                os_id=ordem_de_servico,
                servico_id=id_servico,
                valor_servico=valor_servico
            )
            servico_ordem_servico.save()
            # salva outros possíveis serviços
            if request.POST.get('servico1'):
                print('servico 2 foi')
                id_servico2 = Servico.objects.get(pk=id_servico2)
                servico_ordem_servico = Servico_os(
                    os_id=ordem_de_servico,
                    servico_id=id_servico2,
                    valor_servico=valor_servico2
                )
                servico_ordem_servico.save()
            if request.POST.get('servico2'):
                id_servico3 = Servico.objects.get(pk=id_servico3)
                servico_ordem_servico = Servico_os(
                    os_id=ordem_de_servico,
                    servico_id=id_servico3,
                    valor_servico=valor_servico3
                )
                servico_ordem_servico.save()
            #chama a função que salva os arquivos
            salvar_documentos(arquivo, tipo_doc, ordem_de_servico)
            if request.FILES.get('file1'):
                salvar_documentos(arquivo1, tipo_doc1, ordem_de_servico)
            if request.FILES.get('file2'):
                salvar_documentos(arquivo2, tipo_doc2, ordem_de_servico)
            messages.success(request, 'Ordem de Serviço feita com sucesso!')
    return redirect('ordem_servico')
    # return paginacao(request)

def salvar_documentos(arquivo, tipo_doc, ordem_de_servico):
    if arquivo:
        documento = Documentos(tipo_doc=tipo_doc, arquivo=arquivo, ordem_servico_id=ordem_de_servico)
        documento.save()
    else:
        return

def buscar_cliente(request):
    nome_cliente = request.GET.get("nome")
    lista_clientes = []

    if nome_cliente:
        clientes = Cliente.objects.filter(name__icontains=nome_cliente)[:5]
        for cliente in clientes:
            lista_clientes.append({
                'id': cliente.pk,
                'name': cliente.name,
                'cpfcnpj': cliente.cpf_cnpj,
                'telefone': cliente.telefone,
                'cep': cliente.cep,
                'cidade': cliente.cidade,
                'bairro': cliente.bairro,
                'numero': cliente.numero
            })
    return JsonResponse({'status': 200, 'data': lista_clientes})

# def buscar_cliente(request):
#     nome = request.GET.get('nome', None)
#     if nome:
#         cliente = Cliente.objects.filter(name=nome).first()
#         if cliente:
#             data = {
#                 'id': cliente.pk,
#                 'cpf_cnpj': cliente.cpf_cnpj,
#                 'telefone': cliente.telefone,
#                 'cep': cliente.cep,
#                 'cidade': cliente.cidade,
#                 'bairro': cliente.bairro,
#                 'numero': cliente.numero
#             }
#             return JsonResponse(data)
#     return JsonResponse({})

def buscar_servico(request):
    servico = request.GET.get('servico', None)
    if servico:
        servico_escolhido = Servico.objects.filter(nome=servico).first()
        print('servico escolhido:', servico_escolhido)
        if servico_escolhido:
            data = {
                'id_servico': servico_escolhido.pk,
                'desc': servico_escolhido.descricao,
                'valor_total': servico_escolhido.valor_total,
            }
            return JsonResponse(data)
    return JsonResponse({})

def paginacao(request):
    ordens_servicos = OrdemServico.objects.all().values('id', 'nome_cliente', 'modelo', 'placa', 'status', 'valor_f')
    ordens_servicos_paginados = Paginator(ordens_servicos, 15)
    page_num = request.GET.get('page')
    ordens_servicos = ordens_servicos_paginados.get_page(page_num)

    return render(request, 'os.html', {'ordens_servicos': ordens_servicos})

def excluir_os(request, id):
    if request.method == 'POST':
        ordem_servico = get_object_or_404(OrdemServico, id=id)
        ordem_servico.delete()
        messages.success(request, 'Ordem de serviço excluida com sucesso!')
        return redirect(reverse('ordem_servico'))
    else:
        print('não foi')
        return redirect(reverse('ordem_servico'))

def consultar_os(request, id):
    ordem_servico = get_object_or_404(OrdemServico, pk=id)
    servicos_os = Servico_os.objects.filter(os_id=ordem_servico).select_related('servico_id')
    documentos_da_os = Documentos.objects.filter(ordem_servico_id=ordem_servico)
    datas = {
        'data_aq': (ordem_servico.data_aq.strftime('%Y-%m-%d') if ordem_servico.data_aq else ''),
        'data_servico':ordem_servico.data_servico.strftime('%Y-%m-%d'),
        'data_entrega': (ordem_servico.data_entrega.strftime('%Y-%m-%d') if ordem_servico.data_entrega else ''),
    }
    print(documentos_da_os)
    return render(
        request,
        'consultaos.html',
        {'ordem_servico': ordem_servico,
         'servicos_os': servicos_os,
         'documentos': documentos_da_os,
         'data': datas}
    )

def editar_os(request, id):
    ordem_servico = get_object_or_404(OrdemServico, pk=id)
    servicos_os = Servico_os.objects.filter(os_id=ordem_servico).select_related('servico_id')
    print(f"Serviços da os: {servicos_os}")
    documentos_da_os = Documentos.objects.filter(ordem_servico_id=ordem_servico)
    dados = {'modelo': ordem_servico.modelo,
             'renavam': ordem_servico.renavam,
             'placa': ordem_servico.placa,
             'chassi': ordem_servico.chassi,
             'cor': ordem_servico.cor,
             'combustivel': ordem_servico.combustivel,
             'valor_veiculo': ordem_servico.valor_veiculo,
             'ano_modelo': ordem_servico.ano_modelo,
             'data_aq': (ordem_servico.data_aq.strftime('%Y-%m-%d') if ordem_servico.data_aq else ''),
             'cpf_vendedor': ordem_servico.cpf_vendedor,
             'concessionaria': ordem_servico.concessionaria,
             'tipo_veiculo': ordem_servico.tipo_veiculo,
             'valor_f': ordem_servico.valor_f,
             'desconto': ordem_servico.desconto,
             'pendencias': ordem_servico.pendencias,
             'observacoes': ordem_servico.observacoes,
             'data_servico':ordem_servico.data_servico.strftime('%Y-%m-%d'),
             'data_entrega': (ordem_servico.data_entrega.strftime('%Y-%m-%d') if ordem_servico.data_entrega else ''),
             }
    servicos = Servico.objects.all() #para os tipos de serviços existentes
    return render(
        request,
        'editaros.html',
        {'ordem_servico': ordem_servico,
         'servicos_os': servicos_os,
         'documentos': documentos_da_os,
         'data': dados,
         'servicos': servicos}
    )

def form_edicao_os(request):
    if request.method == 'POST':
        id_ordem_servico = request.POST.get('id_ordem_servico')
        ordem_servico = get_object_or_404(OrdemServico, pk=id_ordem_servico)
        ordem_servico.renavam = request.POST.get('renavam')
        ordem_servico.placa = request.POST.get('placa')
        ordem_servico.valor_veiculo = request.POST.get('valor_veiculo')
        ordem_servico.chassi = request.POST.get('chassi')
        ordem_servico.cor = request.POST.get('cor')
        ordem_servico.combustivel = request.POST.get('combustivel')
        ordem_servico.modelo = request.POST.get('modelo')
        ordem_servico.ano_modelo = request.POST.get('ano_modelo')
        ordem_servico.pendencias = request.POST.get('pendencias')
        ordem_servico.desconto = request.POST.get('desconto')
        ordem_servico.valor_f = request.POST.get('valor_f')
        ordem_servico.data_servico = request.POST.get('data_servico')
        ordem_servico.cpf_vendedor = request.POST.get('cpf_vendedor')
        ordem_servico.concessionaria = request.POST.get('concessionaria')
        ordem_servico.tipo_veiculo = request.POST.get('tipo_veiculo')
        ordem_servico.observacoes = request.POST.get('observacoes')
        if request.POST.get('data_entrega'):
            ordem_servico.data_entrega = request.POST.get('data_entrega')
        if request.POST.get('data_aq'):
            ordem_servico.data_aq = request.POST.get('data_aq')
        ordem_servico.save()

        servicos_os = Servico_os.objects.filter(os_id=ordem_servico)
        for i, servico_os in enumerate(servicos_os, start=1):
            #verificar se existe um serviço que foi alterado:
            servico_id = request.POST.get(f'id_servico_alterado{i}')
            valor_servico = request.POST.get(f'valor_servico{i}')
            if servico_id and valor_servico:
                servico_da_os = Servico.objects.get(pk=servico_id)
                servico_os.servico_id = servico_da_os
                servico_os.valor_servico = valor_servico
                servico_os.save()
        messages.success(request, 'Ordem de Serviço editada com sucesso!')
        return redirect('ordem_servico')
    return redirect('ordem_servico')

def adicionar_servico(request, id):
    ordem_servico = get_object_or_404(OrdemServico, id=id)
    if request.method == 'POST':
        id_servico = request.POST.get('id_novo_servico')
        valor_servico = request.POST.get('valor_servico')
        # buscando o id do servico, porque servico_id em Servico_os tem que ser uma instancia de Servico
        id_servico = get_object_or_404(Servico, id=id_servico)
        novo_servico = Servico_os(os_id=ordem_servico, servico_id=id_servico, valor_servico=valor_servico)
        novo_servico.save()
        messages.success(request, 'Serviço adicionado com sucesso!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        print('erro ao adicionar.')
        return redirect(reverse('home'))


def excluir_servico(request, id):
    print("entrou na função de exclusao de servico")
    if request.method == 'POST':
        id_ordem_servico = request.POST.get('id_ordem_servico')
        servico = get_object_or_404(Servico_os, id=id)
        print('aqui foi')
        servico.delete()
        messages.success(request, 'Serviço excluido com sucesso!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        print('erro ao excluir')
        return redirect(reverse('editar_os'))

def filtrar_documentos(request):
    documentos = Documentos.objects.all()
    for documento in documentos:
        documento.is_image()
        documento.is_pdf()
    
    return render(request, 'consultaos.html', {'documentos': documentos})

def filtrar_os(request):
    tipo = request.GET.get('tipo')
    valor_filtro = request.GET.get('valor_filtro')

    if valor_filtro:
        if tipo == 'nome_cliente':
            os_filtrada = OrdemServico.objects.filter(nome_cliente__icontains=valor_filtro)
        elif tipo == 'id_cliente' and valor_filtro.isdigit():
            os_filtrada = OrdemServico.objects.filter(cliente_id=valor_filtro)
        elif tipo == 'id_os' and valor_filtro.isdigit():
            os_filtrada = OrdemServico.objects.filter(id=valor_filtro)
        elif tipo == 'veiculo':
            os_filtrada = OrdemServico.objects.filter(modelo__icontains=valor_filtro)
        elif tipo == 'status':
            os_filtrada = OrdemServico.objects.filter(status__icontains=valor_filtro)
        else:
            os_filtrada = OrdemServico.objects.filter(placa=valor_filtro)

        if os_filtrada:
            return render(request, 'os.html', {'ordens_servicos': os_filtrada})
        else:
            messages.error(request, 'Nenhum resultado foi encontrado!')
    return redirect('ordem_servico')

def atualizar_status(request):
    if request.method == 'POST':
        id_ordem_servico = request.POST.get('id_ordem_servicos')
        novo_status = request.POST.get('novo_status')
        print('aq ta tudo na paz')
        ordem_servico = get_object_or_404(OrdemServico, pk=id_ordem_servico)

        ordem_servico.status = novo_status
        ordem_servico.save()
        messages.success(request, f'Situação da ordem de serviço {id_ordem_servico} alterado para {novo_status}')
        return redirect('ordem_servico')
    else:
        return paginacao(request)
    
def imprimir_os(request, id):
    ordem_servico = get_object_or_404(OrdemServico, pk=id)
    servicos = Servico_os.objects.filter(os_id=ordem_servico).select_related('servico_id')
    return render(request, 'imprimir_os.html', {'ordem_servico': ordem_servico, 'servicos_os': servicos})

def pdf_export(request, id):
    ordem_servico = get_object_or_404(OrdemServico, pk=id)
    servicos = Servico_os.objects.filter(os_id=ordem_servico).select_related('servico_id')
    site_url = settings.SITE_URL
    datas = {
        'data_aq': (ordem_servico.data_aq.strftime('%Y-%m-%d') if ordem_servico.data_aq else ''),
        'data_servico': ordem_servico.data_servico.strftime('%Y-%m-%d'),
        'data_entrega': (ordem_servico.data_entrega.strftime('%Y-%m-%d') if ordem_servico.data_entrega else ''),
    }
    context = {'ordem_servico': ordem_servico, 
                'servicos_os': servicos,
                'site_url': site_url,
                'data': datas}

    html_string = render_to_string('os-pdf_export.html', context)

    weasyprint_html = weasyprint.HTML(string=html_string)
    pdf = weasyprint_html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ordem_servico_numero{id}.pdf"'

    return response




