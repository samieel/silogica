from django.db import models

class PREMISSAS(models.Model):
    modo = models.CharField(max_length=40)
    reducao = models.CharField(max_length=40)
    extensao1 = models.CharField(max_length=20)
    termo1 = models.CharField(max_length=100)
    termo2 = models.CharField(max_length=100)
    extensao2 = models.CharField(max_length=20)
    termo3 = models.CharField(max_length=100)
    termo4 = models.CharField(max_length=100)
    extensao3 = models.CharField(max_length=20)
    termo5 = models.CharField(max_length=100)
    termo6 = models.CharField(max_length=100)
    
class SINTASSE(models.Model):
    pid = models.IntegerField()
    sintasse = models.CharField(max_length=288)

class REDUCAO(models.Model):
    sid_silogismo = models.IntegerField()
    sid_reducao = models.IntegerField()
