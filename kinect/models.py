from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Treinador(models.Model):
    nome = models.CharField(max_length=100, default='')
    descricao = models.CharField(max_length=30)
    telefone = models.CharField(max_length=20)
    dt_nascimento = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="treinador", default=None)

    def __str__(self):
        return self.nome


class Atleta(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=20)
    dt_nascimento = models.DateField()
    historico = models.TextField()
    genero = models.CharField(max_length=1, default="M")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="atleta", default=None)

    def __str__(self):
        return self.nome


"""class Exercicio(models.Model):
    nome = models.CharField(max_length=100)
    parteDoCorpo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome"""


class Treino(models.Model):
    treinador = models.ForeignKey(Treinador, related_name='treinos', on_delete=models.DO_NOTHING)
    atleta = models.ForeignKey(Atleta, related_name='treinos', on_delete=models.DO_NOTHING)
    treino_descricao = models.TextField()
    avaliacao = models.TextField()


class Sessao(models.Model):
    dt_realizada = models.DateTimeField(auto_now_add=True)
    atleta = models.ForeignKey(Atleta, related_name='sessoes', on_delete=models.DO_NOTHING)
    treino = models.ForeignKey(Treino, related_name='sessoes', on_delete=models.DO_NOTHING)
    #exercicio = models.ForeignKey(Exercicio, related_name='sessoes', on_delete=models.DO_NOTHING)
    def __str__(self):
        return str(self.dt_realizada)



class Tempo(models.Model):
    sessao = models.ForeignKey(Sessao, related_name='tempos', on_delete=models.DO_NOTHING)
    tempo = models.FloatField(default=0)
    toucher = models.TextField(default='Não informado')
    parteDoCorpo = models.TextField(default='Não informado')
    def __str__(self):
        return str(self.tempo)

