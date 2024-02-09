from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Utilizador(models.Model):
   user= models.OneToOneField(User, on_delete=models.CASCADE)
   foto= models.CharField(max_length=800)
   pais= models.CharField(max_length=35)
   ocupacao= models.CharField(max_length=65)
   telemovel = models.CharField(max_length=13)
   def _str_(self):
    return self.user.username + "-" + self.curso + "-" + self.foto


class Modelo(models.Model):
    marca =models.CharField(max_length=120)
    nome_modelo =models.CharField(max_length=250)
    tamanho=models.CharField(max_length=10)
    referência= models.CharField(max_length=200)
    preço =models.CharField(max_length=200)
    data_lançamento = models.DateTimeField('data de lançamento')
    tipo =models.CharField(max_length=64, default='Normal')
    id_user=models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    foto= models.CharField(max_length=800)

    def __str__(self):
     return self.nome_modelo + '|' + self.tipo + '|' + self.marca


class Comentario(models.Model):
    modelo= models.ForeignKey(Modelo, on_delete= models.CASCADE)
    utilizador= models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    texto= models.CharField(max_length=350)
    data= models.DateTimeField('data')
    def __str__(self):
        return self.utilizador + '|' + self.texto + '|' + self.data