from django.urls import path
from . import views as homeviews
from clientes import views as clienteviews
from OS import views as osviews


urlpatterns = [
    path('', homeviews.home, name='home'),
    path('cadastro_clientes', clienteviews.cadastro_clientes, name='cadastro_clientes'),
    path('excluir_cliente/<str:id>/', clienteviews.excluir_cliente, name='excluir_cliente'),
    path('filtro_clientes', clienteviews.filtro_clientes, name='filtro_clientes'),
    path('ordem_servico', osviews.ordem_servico, name='ordem_servico'),
    path('consultar_cliente/<str:id>/', clienteviews.consultar_cliente, name='consultar_cliente'),
    path('newos', osviews.newos, name='newos'),
    path('nova_ordem_de_servico', osviews.nova_ordem_de_servico, name='nova_ordem_de_servico'),
    path('teste', osviews.teste, name='teste'),
    path('buscar_cliente', osviews.buscar_cliente, name='buscar_cliente'),
    path('buscar_servico', osviews.buscar_servico, name='buscar_servico'),
    path('excluir_os/<str:id>/', osviews.excluir_os, name='excluir_os'),
    path('consultar_os/<str:id>/', osviews.consultar_os, name='consultar_os')
]