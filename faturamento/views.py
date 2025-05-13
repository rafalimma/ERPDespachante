from django.shortcuts import render, get_object_or_404, redirect
from .models import Fatura, Pagamento, EventoFatura
from OS.models import OrdemServico
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
import datetime
from datetime import timedelta

# Create your views here.
vencimento = datetime.date.today() + datetime.timedelta(days=3)

def faturamento(request):
    return render(request, 'faturamento.html')

# def criar_fatura(id_os):
#     os = OrdemServico.objects.get(pk=id_os)
#     fatura = Fatura(os=os, status="aberto", forma_pagamento="",
#                     data_vencimento=vencimento, solicitante=None,
#                     tomador=None, n_parcelas=None, valor_final=None)
#     fatura.save()

def atualizar_fatura(request):
    from OS.views import ordem_servico
    if request.method == 'POST':
        print('entroi no ifzão')
        # pega o id_os e ve qual os é relacionada a fatura para aditar
        id_os = request.POST.get('id_os')
        id_os = get_object_or_404(OrdemServico, pk=id_os)
        status = request.POST.get('status_fatura')
        data_vencimento = request.POST.get('data_vencimento')
        n_parcelas = request.POST.get('n_parcelas')
        solicitante = request.POST.get('solicitante')
        tomador = request.POST.get('tomador')
        valor_total = request.POST.get('valor_total')
        fatura = Fatura(os=id_os, status=status, data_vencimento=data_vencimento,
                        n_parcelas=n_parcelas, solicitante=solicitante, tomador=tomador,
                        valor_final=valor_total)
        if not all([valor_total, n_parcelas, solicitante,
                    tomador, data_vencimento, status, id_os]):
            messages.error(request, 'É necessário preencher todos os campos! CAMPOS')
            return redirect('ordem_servico')
        if request.POST.get('contem_pagamento'):
            valor_pago = request.POST.get('valor_pago')
            forma_pagamento = request.POST.get('forma_pagamento')
            data_pagamento = request.POST.get('data_pagamento')
            fatura.save()

            pagamento = Pagamento(fatura=fatura, valor_pago=valor_pago,
                                  forma_pagamento=forma_pagamento, data_pagamento=data_pagamento)
            if not all([fatura, valor_pago, forma_pagamento, data_pagamento]):
                messages.error(request, 'É necessário preencher todos os campos referentes ao pagamento!')
                return redirect('ordem_servico')
            pagamento.save()
        else:
            fatura.save()
            messages.success(request, 'Fatura atualizada com sucesso!')
        return redirect('ordem_servico')

