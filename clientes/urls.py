from django.contrib import admin
from django.urls import path
from . import views as clienteviews

urlpatterns = [
    path('', clienteviews.cadastro_clientes, name='cadastro_clientes'),
]