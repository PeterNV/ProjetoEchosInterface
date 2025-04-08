from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    idade= models.TextField(max_length=255)
    email = models.TextField(max_length=255,default='SOME STRING')
    sobrenome = models.TextField(max_length=255,default='SOME STRING')
    ddi = models.TextField(max_length=255,default='SOME STRING')
    celular = models.TextField(max_length=255,default='SOME STRING')
    sexo = models.TextField(max_length=255,default='SOME STRING')
    cpf = models.TextField(max_length=255,default='SOME STRING')
    senha = models.TextField(max_length=255,default='SOME STRING')
    token = models.CharField(max_length=36, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.nome
class Login(models.Model):
    emaill = models.TextField(max_length=255)
    senhal = models.TextField(max_length=255)
class RGraficos(models.Model):
    datae = models.TextField(max_length=255)
class ESenha(models.Model):
    emaill = models.TextField(max_length=255)
    senhal = models.TextField(max_length=255)
    
class novos_valores(models.Model):
    temp = models.TextField(max_length=255,default='SOME STRING')
    hum = models.TextField(max_length=255,default='SOME STRING')
    luz = models.TextField(max_length=255,default='SOME STRING')
    press = models.TextField(max_length=255,default='SOME STRING')
    gas = models.TextField(max_length=255,default='SOME STRING')
    rpm = models.TextField(max_length=255,default='SOME STRING')
    vento = models.TextField(max_length=255,default='SOME STRING')
    ar = models.TextField(max_length=255,default='SOME STRING')