from django.urls import path
from . import views as homeviews
from clientes import views as clienteviews
from OS import views as osviews
from servicos import views as serviews
from login import views as loginviews
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control

urlpatterns = [
    path('', homeviews.home, name='home'),
    path('clientes', clienteviews.clientes, name='clientes'),
    path('cadastro_clientes', clienteviews.cadastro_clientes, name='cadastro_clientes'),
    path('novo_cliente', clienteviews.novo_cliente, name='novo_cliente'),
    path('excluir_cliente/<str:id>/', clienteviews.excluir_cliente, name='excluir_cliente'),
    path('consultar_cliente/<str:id>/', clienteviews.consultar_cliente, name='consultar_cliente'),
    path('editar_cliente/<str:id>/', clienteviews.editar_cliente, name='editar_cliente'),
    path('form_edicao_cliente', clienteviews.form_edicao_cliente, name='form_edicao_cliente'),
    path('filtro_clientes', clienteviews.filtro_clientes, name='filtro_clientes'),
    path('ordem_servico', osviews.ordem_servico, name='ordem_servico'),
    path('newos', osviews.newos, name='newos'),
    path('nova_ordem_de_servico', osviews.nova_ordem_de_servico, name='nova_ordem_de_servico'),
    path('teste', osviews.teste, name='teste'),
    path('buscar_cliente/', osviews.buscar_cliente, name='buscar_cliente'),
    path('buscar_servico', osviews.buscar_servico, name='buscar_servico'),
    path('excluir_os/<str:id>/', osviews.excluir_os, name='excluir_os'),
    path('consultar_os/<str:id>/', osviews.consultar_os, name='consultar_os'),
    path('editar_os/<str:id>/', osviews.editar_os, name='editar_os'),
    path('form_edicao_os', osviews.form_edicao_os, name='form_edicao_os'),
    path('excluir_servico/<str:id>', osviews.excluir_servico, name='excluir_servico'),
    path('filtrar_os', osviews.filtrar_os, name='filtrar_os'),
    path('atualizar_status', osviews.atualizar_status, name='atualizar_status'),
    path('imprimir_os/<str:id>', osviews.imprimir_os, name='imprimir_os'),
    path('pdf_export/<str:id>', osviews.pdf_export, name='pdf_export'),
    path('servicos', serviews.servicos, name='servicos'),
    path('editar_servico/<str:id>', serviews.editar_servico, name='editar_servico'),
    path('form_edicao_servico', serviews.form_edicao_servico, name='form_edicao_servico'),
    path('novo_servico', serviews.novo_servico, name='novo_servico'),
    path('adicao_servico', serviews.adicao_servico, name='adicao_servico'),
    path('excluir_servico/<str:id>/', serviews.excluir_servico, name='excluir_servico'),
    path('usuarios', loginviews.usuarios, name='usuarios'),
    path('novo_usuario', loginviews.novo_usuario, name='novo_usuario'),
    path('cadastro_usuario', loginviews.cadastro_usuario, name='cadastro_usuario'),
    path('editar_usuario/<str:id>', loginviews.editar_usuario, name='editar_usuario'),
    path('form_edicao_usuario', loginviews.form_edicao_usuario, name='form_edicao_usuario'),
]