from django.db import models
import uuid

class PREMISSAS(models.Model):
    classe = models.CharField(max_length=64, null=True)
    modo = models.CharField(max_length=40)
    reducao = models.CharField(max_length=40)
    extensao1 = models.CharField(max_length=20)
    termo1 = models.CharField(max_length=100)
    n1 = models.CharField(max_length=4)
    termo2 = models.CharField(max_length=100)
    extensao2 = models.CharField(max_length=20)
    termo3 = models.CharField(max_length=100)
    n2 = models.CharField(max_length=4)
    termo4 = models.CharField(max_length=100)
    extensao3 = models.CharField(max_length=20)
    termo5 = models.CharField(max_length=100)
    n3 = models.CharField(max_length=4)
    termo6 = models.CharField(max_length=100)
    
class REDUCAO(models.Model):
    sid_silogismo = models.IntegerField()
    sid_reducao = models.IntegerField()

class ERRO(models.Model):
    err_classe = models.CharField(max_length=64, null=True)
    err_sid = models.IntegerField()
    err_erro = models.CharField(max_length=50)

class CLASSE(models.Model):
    cla_codigo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cla_prof = models.CharField(max_length=100)

class E_CLASSE(models.Model):
    e_codigo = models.CharField(max_length=64)
    e_prof = models.CharField(max_length=100, null=True)
