from django.db import models
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
# Create your models here.
class Usuarios(models.Model):
    #id_usuario é um autoidentificador de usuario no bd
    id_usuario = models.AutoField(primary_key=True)
    nome = models