// from django.shortcuts import render
// from django.http import HttpResponse
// from .models import Cliente
// from django.contrib import messages
// from django.shortcuts import get_object_or_404
// from django.shortcuts import redirect
// from django.urls import reverse
// from django.core.paginator import Paginator

// # Create your views here.
// def teste(request):
//     return render(
//         request,
//         'teste.html'
//     )

// def home(request):
//     return render(
//         request,
//         'home.html',
//     )

// def clientes(request):
//     if request.method == "GET":
//         clientes = Cliente.objects.all()
//         return render(request, 'clientes.html', {'clientes': clientes})
//     elif request.method == "POST":
//         clientes = Cliente.objects.all()
//         name = request.POST.get('name') #entre as aspas vai o name que esta no formulário
//         cpf_cnpj = request.POST.get('cpfcnpj')
//         telefone = request.POST.get('telefone')
//         cliente = Cliente(name=name, cpf_cnpj=cpf_cnpj, telefone=telefone)

//         if name != "" and cpf_cnpj != "" and telefone != "":
//             cliente.save()
//             messages.success(request, 'Cadastro de cliente feito com sucesso!')
//         else:
//             messages.error(request, 'É necessário preencher todos os campos!')
//     clientes = Cliente.objects.all()
//     return render(request, 'clientes.html', {'clientes': clientes})

// #Necessário colocar o @has_permission para não dar
// #falha de segurança
// def excluir_cliente(request, id):
//     cliente = get_object_or_404(Cliente, id=id)
//     cliente.delete()
//     messages.success(request, 'Cliente excluido com sucesso')
//     return redirect(reverse('clientes'))

// def filtro_clientes(request):
//     clientes = Cliente.objects.all()
//     # é feito um fetch na url e tipo e valor_filtro são passadas
//     tipo = request.GET.get('tipo')
//     valor_filtro = request.GET.get('valor_filtro')

//     if tipo == 'nome':
//         cliente_filtrado = Cliente.objects.filter(name__icontains=valor_filtro)
//         if cliente_filtrado:
//             print('filtro por nome')
//             return render(request, 'clientes.html', {'clientes': cliente_filtrado})
//         else:
//             messages.error(request, 'Nenhum resultado foi encontrado!')
//     elif tipo == 'cpf':
//         cliente_filtrado = Cliente.objects.filter(cpf_cnpj=valor_filtro)
//         if cliente_filtrado:
//             return render(request, 'clientes.html', {'clientes': cliente_filtrado})
//         else:
//             messages.error(request, 'Nenhum resultado foi encontrado!')

//     return render(request, 'clientes.html', {'clientes': clientes})

// # def paginacao(request):
// #     clientes = Cliente.objects.all()
// #     clientes_paginados = Paginator(clientes, 8)
// #     page_num = request.GET.get('page')
// #     page = clientes_paginados.get_page(page_num)
// #     return render(request, 'clientes.html', {'page': page})


// Botão de excluir:
//                         <td>
//                             <a href="#"  title="CONSULTAR" style="height: 20px; margin-left: -80px;">
//                                 <img src="{% static 'index/images/consultar.png' %}" style="width: 22px; height: 23px;">
//                             </a>
//                         </td>