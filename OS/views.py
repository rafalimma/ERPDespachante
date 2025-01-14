from django.shortcuts import render, get_object_or_404, redirect
from clientes.models import Cliente
from login.models import Filial
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import OrdemServico, Servico, Servico_os, Documentos, Eventos
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from time import strftime
from django.template.loader import get_template
from django.template.loader import render_to_string 
from datetime import date
import weasyprint # type: ignore
from django.contrib.auth.decorators import login_required
from utils.validador import validador
from django.db.models import Q
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.conf import settings

DEFAULT_DATE = ""

CLIENTES = Cliente.objects.all()
SERVICOS = Servico.objects.all()

def teste(request):
    clientes = Cliente.objects.all()
    servicos = Servico.objects.all()
    return render(request, 'teste.html', {'clientes': clientes, 'servicos': servicos})

@login_required
def ordem_servico(request):
    return paginacao(request)
    # ordens = OrdemServico.objects.all()
    # return render(request, 'os.html', {'ordens_servicos': ordens})

@login_required
def newos(request):
    return render(request, 'newos.html', {'clientes': CLIENTES, 'servicos': SERVICOS})

@login_required
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
            messages.error(request, 'É necessário selecionar um cliente.')
            # capturando os dados do formulário (requsição post passada)
            form_data = request.POST
            return render(request, 'newos.html', {
                'clientes': CLIENTES,
                'servicos': SERVICOS,
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
            form_data = request.POST
            print('indo pro htttp reffer')
            return render(request, 'newos.html', {
                'clientes': CLIENTES,
                'servicos': SERVICOS,
                'form_data': form_data
            })
        elif not validador(cpf_vendedor):
            form_data = request.POST
            messages.error(request, 'O CPF ou CNPJ do vendedor não são válidos.')
            return render(request, 'newos.html', {
                'clientes': CLIENTES,
                'servicos': SERVICOS,
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

@login_required
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

@login_required
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

@login_required
def paginacao(request):
    ordens_servicos = OrdemServico.objects.all().values('id', 'nome_cliente', 'modelo', 'placa', 'status', 'valor_f').order_by('-data_servico')
    ordens_servicos_paginados = Paginator(ordens_servicos, 15)
    page_num = request.GET.get('page')
    ordens_servicos = ordens_servicos_paginados.get_page(page_num)

    return render(request, 'os.html', {'ordens_servicos': ordens_servicos})

@login_required
def excluir_os(request, id):
    if request.method == 'POST':
        ordem_servico = get_object_or_404(OrdemServico, id=id)
        ordem_servico.delete()
        messages.success(request, 'Ordem de serviço excluida com sucesso!')
        return redirect(reverse('ordem_servico'))
    else:
        print('não foi')
        return redirect(reverse('ordem_servico'))

@login_required
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

@login_required
def editar_os(request, id):
    ordem_servico = get_object_or_404(OrdemServico, pk=id)
    servicos_os = Servico_os.objects.filter(os_id=ordem_servico).select_related('servico_id')
    eventos = Eventos.objects.filter(os=id)
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
    return render(
        request,
        'editaros.html',
        {'ordem_servico': ordem_servico,
         'servicos_os': servicos_os,
         'documentos': documentos_da_os,
         'data': dados,
         'servicos': SERVICOS,
         'eventos': eventos}
    )

@login_required
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

@login_required
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

@login_required
def excluir_servico_os(request, id):
    if request.method == 'POST':
        servico = get_object_or_404(Servico_os, id=id)
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
    if request.method == 'POST':
        identificador = request.POST.get('identificador')
        nome = request.POST.get('nome')
        placa = request.POST.get('placa')
        veiculo = request.POST.get('veiculo')
        situacao = request.POST.get('situacao')
        data = request.POST.get('data')

        filtro = Q()
        if identificador:
            filtro &= Q(id=identificador)
        if nome:
            filtro &= Q(nome_cliente__icontains=nome)
        if veiculo:
            filtro &= Q(modelo__icontains=veiculo)
        if placa:
            filtro &= Q(placa__icontains=placa)
        if situacao:
            filtro &= Q(status=situacao)
        if data:
            filtro &= Q(data_servico=data)

        if not any([identificador, nome, placa, veiculo, situacao, data]):
            messages.warning(request, 'Preencha pelo menos um campo para realizar a busca.')
            return redirect('ordem_servico')

        ordem_servico = OrdemServico.objects.filter(filtro)
        if ordem_servico.exists():
            return render(request, 'os.html', {'ordens_servicos': ordem_servico})
        else:
            print('foi no elseee')
            messages.error(request, 'Nenhum resultado foi encontrado!')
    return redirect('ordem_servico')

@login_required
def atualizar_status(request):
    if request.method == 'POST':
        id_ordem_servico = request.POST.get('id_ordem_servicos')
        novo_status = request.POST.get('novo_status')
        status_anterior = request.POST.get('atual_status')
        observacoes = request.POST.get('observacoes')
        documento = request.FILES.get('file')
        ordem_servico = OrdemServico.objects.get(id=id_ordem_servico)

        ordem_servico.status = novo_status
        ordem_servico.save()
        evento = Eventos(os=ordem_servico, status_anterior=status_anterior,
                         status_atual=novo_status, observacoes=observacoes,
                         arquivo=documento)
        evento.save()
        messages.success(request, f'Situação da ordem de serviço {id_ordem_servico} alterado para {novo_status}')
        return redirect('ordem_servico')
    else:
        return paginacao(request)

@login_required
def imprimir_os(request, id):
    ordem_servico = get_object_or_404(OrdemServico, pk=id)
    servicos = Servico_os.objects.filter(os_id=ordem_servico).select_related('servico_id')
    return render(request, 'imprimir_os.html', {'ordem_servico': ordem_servico, 'servicos_os': servicos})

def pdf_export(request, id):
    ordem_servico = get_object_or_404(OrdemServico, pk=id)
    servicos = Servico_os.objects.filter(os_id=ordem_servico).select_related('servico_id')
    filial = Filial.objects.first()
    # print(filial)
    # filial_logo = filial.logo if filial else "Nenhuma filial encontrada"
    # print(filial_logo)
    # filial_logo_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{filial_logo}")
    # print(filial_logo_url)
    datas = {
        'data_aq': (ordem_servico.data_aq.strftime('%d/%m/%Y') if ordem_servico.data_aq else ''),
        'data_servico': ordem_servico.data_servico.strftime('%d/%m/%Y'),
        'data_entrega': (ordem_servico.data_entrega.strftime('%d/%m/%Y') if ordem_servico.data_entrega else ''),
    }
    context = {'ordem_servico': ordem_servico, 
                'servicos_os': servicos,
                'data': datas,
                'filial': filial}

    html_string = render_to_string('os-pdf_export.html', context)
    # isso serve para substituir no html a logo em base64 ja que em prod é a unica maneira que da certo
    # para a visualização exsite uma imagem de contingência que aparece porque image/logo vai dar erro
    # html_string = html_string.replace(
    #     "logo",
    #     filial_logo
    # )
    # base_url = request.build_absolute_uri(settings.MEDIA_URL)
    weasyprint_html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = weasyprint_html.write_pdf()
    

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ordem_servico_numero{id}.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'

    return response

@login_required
def adicionar_documento(request, id):
    if request.method == 'POST':
        ordem_servico = get_object_or_404(OrdemServico, id=id)
        tipo_doc = request.POST.get('tipo_doc')
        arquivo = request.FILES.get('new_file')

        salvar_documentos(arquivo, tipo_doc, ordem_servico)
        messages.success(request, 'Documento salvo com sucesso!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        print('ocorreu um erro ao salvar')
        return redirect(reverse('home'))
    
@login_required
def excluir_documento(request, id):
    if request.method == 'POST':
        print('foi carai')
        documento = get_object_or_404(Documentos, id=id)
        documento.delete()
        messages.success(request, 'Documento excluido com sucesso!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(reverse('editar_os'))







