from django.contrib import admin
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
# Register your models here.
from django.contrib import admin
from .models import Filial

@admin.register(Filial)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'logo', 'logo_base64', 'telefone', 'endereco')