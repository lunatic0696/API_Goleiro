from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.db.models import Subquery
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from chartjs.views.lines import BaseLineChartView
from rest_pandas import PandasView, PandasSerializer, PandasSimpleView

# Create your views here.
from django.template import loader
from django.utils.decorators import *
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import \
    IsAuthenticated  # << Adicionar como permission_classes de uma view para ver apenas quando autenticado
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime

from kinect.forms import *
from kinect.models import *
from kinect.serializer import *

def atleta_check(user):
    if user.groups.filter(name='Atletas'):
        return True
    else:
        return False

def treinador_check(user):
    if user.groups.filter(name='Treinadores'):
        return True
    else:
        return False

class AtletaList(APIView):

    def get(self, request):
        queryset = Atleta.objects.all()
        serializer_class = AtletaSerializer(queryset, many=True)
        return Response(serializer_class.data)


class TreinadorList(APIView):

    def get(self, request):
        queryset = Treinador.objects.all()
        serializer_class = TreinadorSerializer(queryset, many=True)
        return Response(serializer_class.data)


class TreinadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Treinador.objects.all()
    serializer_class = TreinadorSerializer


class TreinadorSessoes(APIView):
    def get(self, request, treinadorid):
        treinador = Treinador.objects.get(id=treinadorid)
        s = []
        queryset = Sessao.objects.all()
        for i in queryset:
            if i.treino.treinador == treinador:
                s.append(i)
        serializer_class = SessaoSerializer(s, many=True)
        return Response(serializer_class.data)


class TreinadorAtletas(APIView):
    def get(self, request, treinadorid):
        treinador = Treinador.objects.get(id=treinadorid)
        treinos = Treino.objects.filter(treinador=treinador)
        p = []
        for i in treinos:
            if i.atleta not in p:
                p.append(i.atleta)
        serializer_class = AtletaSerializer(p, many=True)
        return Response(serializer_class.data)


"""
class ExercicioList(APIView):
    # Tem que ter essa vírgula no final se for só uma classe, senão o Django reconhece como String, e não como Tuple
    permission_classes = IsAuthenticated,

    def get(self, request):
        queryset = Exercicio.objects.all()
        serializer_class = ExercicioSerializer(queryset, many=True)
        return Response(serializer_class.data)
"""

class TreinoList(APIView):

    def get(self, request):
        queryset = Treino.objects.all()
        serializer_class = TreinoSerializer(queryset, many=True)
        return Response(serializer_class.data)


class AtletaSessoes(APIView):
    def get(self, request, atletaid):
        atleta = Atleta.objects.get(id=atletaid)
        queryset = atleta.sessoes.all()
        serializer_class = SessaoSerializer(queryset, many=True)
        return Response(serializer_class.data)


class MakeSessao(APIView):
    def post(self, request, treinoid):
        treino = Treino.objects.get(id=treinoid)
        #exercicio = Exercicio.objects.get(id=exerid)
        atleta = treino.atleta
        sessao = Sessao(treino=treino, atleta=atleta ,dt_realizada=datetime.now())
        sessao.save()
        serializer_class = SessaoSerializer(sessao, many=False)
        return Response(serializer_class.data)


class MakeTempo(APIView):
    def post(self, request, sessaoid):
        print(request.data)
        tempo = request.data['tempo']
        parteDoCorpo = request.data['parteDoCorpo']
        sessao =  Sessao.objects.get(id=sessaoid)
        toucher = request.data['toucher']
        print(parteDoCorpo)
        tempoobject = Tempo(tempo=tempo, parteDoCorpo=parteDoCorpo, toucher=toucher, sessao=sessao)
        serializer_class = TempoSerializer(tempoobject, many=False)
        tempoobject.save()
        print(tempoobject)
        return Response(serializer_class.data)


class CadastroTreinador(APIView):
    def post(self, request):
        form = TreinadorForm(request.POST)
        if form.is_valid():
            form.clean()
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['nome'],
                                            last_name=form.cleaned_data['sobrenome'])
            nomefull = form.cleaned_data['nome']+' '+form.cleaned_data['sobrenome']
            treinador = Treinador(nome=nomefull,
                                   #clinica=form.cleaned_data['clinica'],
                                   #crm=form.cleaned_data['crm'],
                                   descricao=form.cleaned_data['descricao'],
                                   telefone=form.cleaned_data['telefone'],
                                   dt_nascimento=form.cleaned_data['dt_nascimento'],
                                   user=user)
            if not Group.objects.get(name='Treinadores'):
                Group.objects.create(name='Treinadores')
            fgroup = Group.objects.get(name='Treinadores')
            user.groups.add(fgroup)
            treinador.save()
            return HttpResponse("Treinador cadastrado.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = TreinadorForm()
        return render(request, 'cadastrotreinador.html', {'form':form})

class CadastroAtleta(APIView):
    def post(self, request):
        form = AtletaForm(request.POST)
        if form.is_valid():
            form.clean()
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['nome'],
                                            last_name=form.cleaned_data['sobrenome'])
            nomefull = form.cleaned_data['nome'] + ' ' + form.cleaned_data['sobrenome']
            atleta = Atleta(nome=nomefull,
                                   cpf=form.cleaned_data['cpf'],
                                   genero=form.cleaned_data['genero'],
                                   historico=form.cleaned_data['historico'],
                                   telefone=form.cleaned_data['telefone'],
                                   dt_nascimento=form.cleaned_data['dt_nascimento'],
                                   user=user)
            atleta.save()
            if not Group.objects.get(name='Atletas'):
                Group.objects.create(name='Atletas')
            pgroup = Group.objects.get(name='Atletas')
            user.groups.add(pgroup)
            return HttpResponse("Atleta cadastrado.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = AtletaForm()
        return render(request, 'cadastroatleta.html', {'form': form})

"""
class RegistrarExercicio(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return treinador_check(self.request.user)
    def post(self, request):
        form = ExercicioForm(request.POST)
        if form.is_valid():
            form.clean()
            exercicio = Exercicio(nome=form.cleaned_data['nome'], parteDoCorpo=form.cleaned_data['parteDoCorpo'])
            exercicio.save()
            return HttpResponse("Exercício registrado com sucesso.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = ExercicioForm()
        return render(request, 'registrarexercicio.html', {'form':form})
"""

class RegistrarTreino(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return treinador_check(self.request.user)
    def post(self, request):
        form = TreinoForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.clean()
            treinador = Treinador.objects.get(user=request.user)
            treino = Treino(treinador=treinador, atleta=form.cleaned_data['atleta'], treino_descricao=form.cleaned_data['treino_descricao'])
            treino.save()
            responsestring = "Treino registrado com sucesso.\nO código do treino é:"+str(treino.id)
            return HttpResponse(responsestring)
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = TreinoForm()
        return render(request, 'registrartreino.html', {'form':form})

class RegistrarTreinoViaID(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return treinador_check(self.request.user)
    def post(self, request):
        form = TreinoViaIDForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.clean()
            treinador = Treinador.objects.get(user=request.user)
            if Atleta.objects.filter(id=form.cleaned_data['atletaid']).exists():
                atleta = Atleta.objects.get(id=form.cleaned_data['atletaid'])
                treino = Treino(treinador=treinador, atleta=atleta, treino_descricao=form.cleaned_data['treino_descricao'])
                treino.save()
                responsestring = "Treino registrado com sucesso.\nO código do treino é:"+str(treino.id)
                return HttpResponse(responsestring)
            else:
                return HttpResponse("ID fornecida não encontrada entre os atletas.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = TreinoViaIDForm()
        return render(request, 'registrartreino.html', {'form':form})

class RegistrarAvaliacaoTreino(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return treinador_check(self.request.user)
    def post(self, request):
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            form.clean()
            treino = Treino.objects.get(id=form.cleaned_data['treinoid'])
            treinador = Treinador.objects.get(user=request.user)
            if treino.treinador==treinador:
                treino.avaliacao = form.cleaned_data['avaliacao']
                treino.save(update_fields=['avaliacao'])
                return HttpResponse("Treino atualizado com sucesso.")
            else:
                return HttpResponse("Erro ao obter treinador ou o treinador logado não é o responsável por esse treino.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = AvaliacaoForm()
        return render(request, 'treinoavaliacao.html', {'form':form})

class RegistrarAvaliacaoDireta(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return treinador_check(self.request.user)
    def post(self, request, treinoid):
        form = AvaliacaoDiretaForm(request.POST)
        if form.is_valid():
            form.clean()
            treino = Treino.objects.get(id=treinoid)
            treinador = Treinador.objects.get(user=request.user)
            if treino.treinador==treinador:
                treino.avaliacao = form.cleaned_data['avaliacao']
                treino.save(update_fields=['avaliacao'])
                return HttpResponse("Treino atualizado com sucesso.")
            else:
                return HttpResponse("Erro ao obter treinador ou o treinador logado não é o responsável por esse treino.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request, treinoid):
        form = AvaliacaoDiretaForm()
        treino = Treino.objects.get(id=treinoid)
        return render(request, 'treinoavaliacao.html', {'form':form, 'treino':treino})


class LoginTreinador(APIView):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            form.clean()
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                for treinador in Treinador.objects.all():
                    if treinador.user == user:
                        login(request, user)
                        return redirect('indextreinador')
                return HttpResponse("Usuário não é Treinador.")
            return HttpResponse("Usuário não encontrado.")
        else:
            return render(request, 'logintreinador.html', {'form': form})
    def get(self, request):
        form = LoginForm()
        return render(request, 'logintreinador.html', {'form': form})

class LoginAtleta(APIView):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            form.clean()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                for atleta in Atleta.objects.all():
                    if atleta.user == user:
                        login(request, user)
                        return redirect('indexatleta')
                return HttpResponse("Usuário não é Atleta.")
            return HttpResponse("Usuário não encontrado.")
        else:
            return render(request, 'loginatleta.html', {'form': form})

    def get(self, request):
        form = LoginForm()
        return render(request, 'loginatleta.html', {'form': form})

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('index')

class TreinadorTreinos(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return treinador_check(self.request.user)
    def get(self, request):
        if request.user.is_authenticated:
            currentuser = request.user
            treinador = Treinador.objects.get(user=currentuser.id)
            list = Treino.objects.filter(treinador=treinador)
            return render(request, 'treinadortreinos.html', {'list': list})
        else:
            return HttpResponse("Algo deu errado, tente novamente")


class AtletaTreinos(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return atleta_check(self.request.user)
    def get(self, request):
        if request.user.is_authenticated:
            currentuser = request.user
            atleta = Atleta.objects.get(user=currentuser.id)
            list = Treino.objects.filter(atleta=atleta)
            return render(request, 'atletatreinos.html', {'list': list})
        else:
            return HttpResponse("Algo deu errado, tente novamente")

class TreinoDetalhe(LoginRequiredMixin, APIView):
    def get(self, request, treinoid):
        treino = Treino.objects.get(id=treinoid)
        sessoes = Sessao.objects.filter(treino=treino)
        if treino.treinador.user == request.user or treino.atleta.user == request.user:
            return render(request, 'treinodetalhe.html', {'treino': treino, 'sessoes': sessoes, 'treinoid':treinoid})
        else:
            return HttpResponse("Você não tem acesso a esse treino.")

class SessaoDetalhe(LoginRequiredMixin, APIView):
    def get(self, request, sessaoid):
        sessao = Sessao.objects.get(id=sessaoid)
        tempos = Tempo.objects.filter(sessao=sessao)
        if sessao.treino.treinador.user == request.user or sessao.treino.atleta.user == request.user:
            return render(request, 'sessaodetalhe.html', {'sessao': sessao, 'tempos': tempos, 'sessaoid':sessaoid})
        else:
            return HttpResponse("Você não tem acesso a essa sessão.")

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return []

    def get_providers(self):
        """Return names of datasets."""
        #return ["Central", "Eastside", "Westside"]
        return ["Média"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

class TemposGraphView(APIView):
    def get(self, request, sessaoid):
        return render(request, 'chartdemo.html', {'sessaoid': sessaoid})

class TemposGraphJSONView(BaseLineChartView):

    def get_labels(self):
        #return ['1','2','3','4']
        array = []
        for label in Tempo.objects.filter(sessao=self.kwargs['sessaoid']).values_list('parteDoCorpo', flat=True).distinct():
            labelarray = []
            for t in Tempo.objects.filter(sessao=self.kwargs['sessaoid']):
                if t.parteDoCorpo == label:
                    labelarray.append(t.tempo)
            array.append(labelarray)
        maxlength = 0
        for list in array:
            if len(list)>maxlength:
                maxlength = len(list)
        labels = []
        for i in range(1, maxlength+1):
            labels.append(i)
        print(labels)
        return labels

    def get_providers(self):
        print(Tempo.objects.filter(sessao=self.kwargs['sessaoid']).values_list('parteDoCorpo', flat=True).distinct())
        return Tempo.objects.filter(sessao=self.kwargs['sessaoid']).values_list('parteDoCorpo', flat=True).distinct()

    def get_data(self):
        array = []
        for label in Tempo.objects.filter(sessao=self.kwargs['sessaoid']).values_list('parteDoCorpo', flat=True).distinct():
            labelarray = []
            for t in Tempo.objects.filter(sessao=self.kwargs['sessaoid']):
                if t.parteDoCorpo == label:
                    labelarray.append(t.tempo)
            array.append(labelarray)
        #tempos = Tempo.objects.filter(sessao=self.kwargs['sessaoid']).distinct()
        print(array)
        return array

class SessaoGraphView(APIView):
    def get(self, request, treinoid):
        return render(request, 'chartdemo.html', {'treinoid': treinoid})

class SessaoGraphJSONView(BaseLineChartView):

    def get_labels(self):
        #return ['1','2','3','4']
        labels = []
        sessoes = []
        for sessao in Sessao.objects.filter(treino=self.kwargs['treinoid']):
            tempos = []
            for tempo in Tempo.objects.filter(sessao=sessao):
                tempos.append(tempo)
            sessoes.append(tempos)
        maxlength = 0
        for sessaotempos in sessoes:
            if len(sessaotempos)>maxlength:
                maxlength=len(sessaotempos)
        for i in range(0, maxlength):
            labels.append(i)
        return labels

    def get_providers(self):
        maxlength = len(Sessao.objects.filter(treino=self.kwargs['treinoid']).order_by('dt_realizada'))
        providers = []
        for i in range(1, maxlength+1):
            providers.append("Sessão "+str(i))
        return providers

    def get_data(self):
        array = []
        for sessao in Sessao.objects.filter(treino=self.kwargs['treinoid']).order_by('dt_realizada'):
            sessaoarray = []
            for t in Tempo.objects.filter(sessao=sessao):
                sessaoarray.append(t.tempo)
            array.append(sessaoarray)
        print(array)
        return array

#class TemposGraphView(PandasView):
#    queryset = Tempo.objects.all()
#    def filter_queryset(self, queryset):
#        return queryset.filter(sessao=self.kwargs['sessaoid'])
#    serializer_class = TempoSerializer
#    pandas_serializer_class = PandasSerializer


class PopularDB(LoginRequiredMixin, APIView):
    def post(self, request):
        usertreinador1 = User.objects.create_user(username='treinador1', password='treinador1',
                                              email='treinador1@teste.com')  # Treinador1User
        usertreinador2 = User.objects.create_user(username='treinador2', password='treinador2',
                                              email='treinador2@teste.com')  # Treinador2User
        userpac1 = User.objects.create_user(username='pac1', password='pac1', email='pac1@teste.com')  # Atleta1User
        userpac2 = User.objects.create_user(username='pac2', password='pac2', email='pac2@teste.com')  # Atleta2User
        userpac3 = User.objects.create_user(username='pac3', password='pac3', email='pac3@teste.com')  # Atleta3User
        treinador1 = Treinador(nome='Treinador1', clinica='Teste', crm='Teste', telefone='Teste',
                                descricao='Teste', dt_nascimento='2000-01-01', user=usertreinador1)
        treinador2 = Treinador(nome='Treinador2', clinica='Teste', crm='Teste', telefone='Teste',
                                descricao='Teste', dt_nascimento='2000-01-01', user=usertreinador2)
        pac1 = Atleta(nome='Atleta1', cpf='Teste', telefone='Teste', historico='Teste',
                        dt_nascimento='2000-01-01', genero='M', user=userpac1)
        pac2 = Atleta(nome='Atleta2', cpf='Teste', telefone='Teste', historico='Teste',
                        dt_nascimento='2000-01-01', genero='M', user=userpac2)
        pac3 = Atleta(nome='Atleta3', cpf='Teste', telefone='Teste', historico='Teste',
                        dt_nascimento='2000-01-01', genero='F', user=userpac3)
        treinador1.save()
        treinador2.save()
        pac1.save()
        pac2.save()
        pac3.save()
        t1 = Treino(treinador=treinador1, atleta=pac1, treino_descricao='Teste', avaliacao='Teste')
        t2 = Treino(treinador=treinador1, atleta=pac1, treino_descricao='Teste', avaliacao='Teste')
        t3 = Treino(treinador=treinador2, atleta=pac2, treino_descricao='Teste', avaliacao='Teste')
        t4 = Treino(treinador=treinador1, atleta=pac3, treino_descricao='Teste', avaliacao='Teste')
        t5 = Treino(treinador=treinador2, atleta=pac3, treino_descricao='Teste', avaliacao='Teste')
        t1.save()
        t2.save()
        t3.save()
        t4.save()
        t5.save()
        #e1 = Exercicio(nome='Teste1', partedocorpo='Teste1')
        #e2 = Exercicio(nome='Teste2', partedocorpo='Teste2')
        #e1.save()
        #e2.save()
        s1 = Sessao(atleta=pac1, treino=t1, dt_realizada='2000-01-01')
        s2 = Sessao(atleta=pac1, treino=t2, dt_realizada='2000-01-01')
        s3 = Sessao(atleta=pac2, treino=t3, dt_realizada='2000-01-01')
        s4 = Sessao(atleta=pac3, treino=t4, dt_realizada='2000-01-01')
        s5 = Sessao(atleta=pac3, treino=t5, dt_realizada='2000-01-01')
        s6 = Sessao(atleta=pac3, treino=t5, dt_realizada='2000-01-01')
        s1.save()
        s2.save()
        s3.save()
        s4.save()
        s5.save()
        s6.save()
