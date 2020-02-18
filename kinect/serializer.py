from rest_framework import serializers
from django.contrib.auth.models import User

from kinect.models import *


class AtletaSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Atleta
        fields =('id', 'user', 'nome', 'telefone', 'cpf', 'dt_nascimento', 'historico', 'genero')

class TreinadorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Treinador
        fields =('id', 'user', 'nome', 'telefone', 'clinica', 'descricao', 'crm', 'dt_nascimento')

"""
class ExercicioSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Exercicio
        fields =('id', 'user', 'nome', 'parteDoCorpo')
"""

class TreinoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Treino
        fields =('id', 'user', 'treinador', 'atleta', 'condicao', 'avaliacao')

class SessaoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Sessao
        fields =('id', 'user', 'dt_realizada', 'treino', 'exercicio')

class TempoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Tempo
        fields =('id', 'user', 'sessao', 'tempo')
