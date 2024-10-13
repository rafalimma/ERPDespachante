from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator
from OS.models import OrdemServico
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
# Create your views here.
def teste(request):
    return render(
        request,
        'teste.html'
    )

def paginacao(request):
    clientes = Cliente.objects.all().values('id', 'name', 'cpf_cnpj', 'telefone')
    clientes_paginados = Paginator(clientes, 15)
    page_num = request.GET.get('page')
    clientes = clientes_paginados.get_page(page_num)

    return render(request, 'clientes.html', {'clientes': clientes})

def consultar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    ordem_servico = OrdemServico.objects.filter(cliente_id=id)
    return render(
        request,
        'consulta.html',
        {'cliente': cliente,
         'ordem_servicos': ordem_servico}
    )

def novo_cliente(request):
    return render(request, 'novo_cliente.html')

def clientes(request):
    return paginacao(request)

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    return render(
        request,
        'editar_cliente.html',
        {'cliente': cliente} 
    )

def form_edicao_cliente(request):
    if request.method == "POST":
        id_cliente = request.POST.get('id_cliente')
        cliente = get_object_or_404(Cliente, pk=id_cliente)
        cliente.name = request.POST.get('name') #entre as aspas vai o name que esta no formulário
        cliente.cpf_cnpj = request.POST.get('cpfcnpj')
        cliente.telefone = request.POST.get('telefone')
        cliente.cep = request.POST.get('cep')
        cliente.cidade = request.POST.get('cidade')
        cliente.bairro = request.POST.get('bairro')
        cliente.numero = request.POST.get('numero')
        cliente.email = request.POST.get('email')
        cliente.estado = request.POST.get('estado')
        if cliente.name == '' or cliente.cpf_cnpj == '':
            messages.error(request, 'Os dados não podem ser nulos!')
            return redirect(f"editar_cliente/{id_cliente}")
        cliente.save()
        messages.success(request, 'Cliente editado com sucesso!')
        return redirect('clientes')
    return redirect('clientes')


def cadastro_clientes(request):
    if request.method == "POST":
        name = request.POST.get('name') #entre as aspas vai o name que esta no formulário
        cpf_cnpj = request.POST.get('cpfcnpj')
        telefone = request.POST.get('telefone')
        cep = request.POST.get('cep')
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        email = request.POST.get('email')
        estado = request.POST.get('estado')

        cliente = Cliente(name=name, cpf_cnpj=cpf_cnpj, telefone=telefone, 
                        cep=cep, cidade=cidade, bairro=bairro, numero=numero,
                        email=email, estado=estado)

        if not all([name, telefone, cpf_cnpj]):
            messages.error(request, 'É necessário preencher todos os campos!')
            form_data = request.POST
            return render(request, 'novo_cliente.html', {'form_data': form_data})
        else:
            cliente.save()
            messages.success(request, 'Cadastro de cliente feito com sucesso!')
    return paginacao(request)

#Necessário colocar o @has_permission para não dar
#falha de segurança
def excluir_cliente(request, id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=id)
        cliente.delete()
        messages.success(request, 'Cliente excluido com sucesso')
        return redirect(reverse('cadastro_clientes'))
    else:
        print('não foi')
        return redirect(reverse('cadastro_clientes'))

def filtro_clientes(request):
    # é feito um fetch na url e tipo e valor_filtro são passadas (java-script)
    tipo = request.GET.get('tipo')
    valor_filtro = request.GET.get('valor_filtro')

    if tipo == 'nome':
        cliente_filtrado = Cliente.objects.filter(name__icontains=valor_filtro)
        if cliente_filtrado:
            print('filtro por nome')
            return render(request, 'clientes.html', {'clientes': cliente_filtrado})
        else:
            messages.error(request, 'Nenhum resultado foi encontrado!')
    elif tipo == 'cpf':
        cliente_filtrado = Cliente.objects.filter(cpf_cnpj=valor_filtro)
        if cliente_filtrado:
            return render(request, 'clientes.html', {'clientes': cliente_filtrado})
        else:
            messages.error(request, 'Nenhum resultado foi encontrado!')

    return paginacao(request)



