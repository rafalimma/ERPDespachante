from django.shortcuts import render, get_object_or_404, redirect
from clientes.models import Cliente
from django.http import JsonResponse
from .models import OrdemServico, Servico, Servico_os, Documentos
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse

# Create your views here.
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control

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
        pendencias = request.POST.get('ano')
        data_entrega = request.POST.get('dtentrega')
        desconto = request.POST.get('desconto')
        valor_f = request.POST.get('vfinal')
        id_servico = request.POST.get('id_servico')
        valor_servico = request.POST.get('valorservico')

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
            messages.error(request, 'É necessário preencher todos os campos!')
            clientes = Cliente.objects.all()
            servicos = Servico.objects.all()
            return render(request, 'newos.html', {'clientes': clientes, 'servicos': servicos})
        if not data_aq:
            data_aq = None
        if not data_entrega:
            data_entrega = None
        # pega a chave primária dos clientes
        cliente = Cliente.objects.get(pk=id_cliente)

        ordem_de_servico = OrdemServico(
            nome_cliente=name, cliente_id=cliente, renavam=renavam,
            placa=placa, chassi=chassi,
            cor=cor, combustivel=combustivel, data_aq=data_aq,
            modelo=modelo, valor_veiculo=valor, ano_modelo=ano_veiculo,
            pendencias=pendencias, data_entrega=data_entrega,
            desconto=desconto, valor_f=valor_f
            )
        if not all([renavam, placa, cliente, id_cliente, name,
                     valor, combustivel, modelo, ano_veiculo, id_servico,
                     valor_servico, valor_f]):
            messages.error(request, 'É necessário preencher todos os campos!')
            clientes = Cliente.objects.all()
            servicos = Servico.objects.all()
            return render(request, 'newos.html', {'clientes': clientes, 'servicos': servicos})
        else:
            # salva o serviço padrão
            ordem_de_servico.save()
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
    
    return paginacao(request)
    # ordens = OrdemServico.objects.all()
    # return render(request, 'os.html', {'ordens_servicos': ordens})

def salvar_documentos(arquivo, tipo_doc, ordem_de_servico):
    if arquivo:
        documento = Documentos(tipo_doc=tipo_doc, arquivo=arquivo, ordem_servico_id=ordem_de_servico)
        documento.save()
    else:
        return

def buscar_cliente(request):
    nome = request.GET.get('nome', None)
    if nome:
        cliente = Cliente.objects.filter(name=nome).first()
        if cliente:
            data = {
                'id': cliente.pk,
                'cpf_cnpj': cliente.cpf_cnpj,
                'telefone': cliente.telefone,
                'cep': cliente.cep,
                'cidade': cliente.cidade,
                'bairro': cliente.bairro,
                'numero': cliente.numero
            }
            return JsonResponse(data)
    return JsonResponse({})

def buscar_servico(request):
    servico = request.GET.get('servico', None)
    if servico:
        descricao = Servico.objects.filter(descricao=servico).first()
        if descricao:
            data = {
                'id_servico': descricao.pk,
                'valor_total': descricao.valor_total,
            }
            return JsonResponse(data)
    return JsonResponse({})

def paginacao(request):
    ordens_servicos = OrdemServico.objects.all().values('id', 'nome_cliente', 'modelo', 'placa', 'cor', 'valor_f')
    ordens_servicos_paginados = Paginator(ordens_servicos, 10)
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
    servico = get_object_or_404(Servico_os, fk=id)
    return render(
        request,
        'consultaos.html',
        {'ordem_servico': ordem_servico,
         'servicos': servico}
    )
