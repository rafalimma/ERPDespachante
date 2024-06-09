from django.contrib import admin
from django.urls import path
from . import views as clienteviews
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
urlpatterns = [
    path('', clienteviews.cadastro_clientes, name='cadastro_clientes'),
]