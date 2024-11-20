from django.db import models
from datetime import date
import json
# Create your models here.

class Relatorios(models.Model):
    tipo = models.CharField(max_length=100)
    meses = models.TextField()
    quantidade = models.TextField()
    data_atualizacao = models.DateTimeField(auto_now_add=True)

# transformando tudo em json pra salvar com string

    def set_meses(self, meses_list):
        self.meses = json.dumps(meses_list)

    def get_meses(self):
        return json.loads(self.meses)

    def set_quantidade(self, quantidade_list):
        self.quantidade = json.dumps(quantidade_list)

    def get_quantidade(self):
        return json.loads(self.quantidade)

    