from django.db import models

# Create your models here.
class Usuarios(models.Model):
    #id_usuario é um autoidentificador de usuario no bd
    id_usuario = models.AutoField(primary_key=True)
    nome = models