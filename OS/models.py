from django.db import models
from clientes.models import Cliente
import datetime
from django.utils import timezone

# Create your models here.
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
class OrdemServico(models.Model):
    renavam = models.IntegerField()
    placa = models.CharField(max_length=7)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nome_cliente = models.CharField(max_length=40)
    chassi = models.CharField(max_length=30, default='')
    cor = models.CharField(max_length=14, default='')
    combustivel = models.CharField(max_length=15, default='')
    modelo = models.CharField(max_length=25, default='')
    valor_veiculo = models.CharField(max_length=6, default='')
    ano_modelo = models.CharField(max_length=5, default='')
    pendencias = models.CharField(max_length=40, default='')
    data_entrega = models.DateField(null=True, blank=True)
    data_aq = models.DateField(null=True, blank=True)
    data_servico = models.DateField(default=datetime.date.today)
    desconto = models.CharField(max_length=10, default='')
    valor_f = models.CharField(max_length=10, default='')


class Servico(models.Model):
    descricao = models.CharField(max_length=50)
    custo = models.CharField(max_length=10)
    valor_liquido = models.CharField(max_length=10)
    valor_total = models.CharField(max_length=10)

class Servico_os(models.Model):
    os_id = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    servico_id = models.ForeignKey(Servico, on_delete=models.CASCADE)
    valor_servico = models.CharField(max_length=10, default='')

class Documentos(models.Model):
    tipo_doc = models.CharField(max_length=30, default='')
    arquivo = models.FileField(upload_to='documents/')
    ordem_servico_id = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tipo_doc
