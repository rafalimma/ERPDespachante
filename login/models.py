from django.db import models
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
# Create your models here.
class Usuarios(models.Model):
    #id_usuario é um autoidentificador de usuario no bd
    id_usuario = models.AutoField(primary_key=True)
    nome = models

class Filial(models.Model):
    nome = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=25, default='')
    logo = models.ImageField(upload_to='clients_image/')
    logo_base64 = models.TextField()
    telefone = models.CharField(max_length=50)
    endereco = models.CharField(max_length=100)
    bairro = models.CharField(max_length=50, default='')
    cidade = models.CharField(max_length=50, default='')