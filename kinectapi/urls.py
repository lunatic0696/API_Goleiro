"""kinectapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt import views as jwt_views

from kinect import views
from kinect.views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('api/atletas/', AtletaList.as_view(), name='atletalist'),
    path('api/treinadores/', TreinadorList.as_view(), name='treinadorlist'),
    path('api/treinadores/<int:pk>', TreinadorDetail.as_view(), name='treinadordetail'),
    path('api/treinadores/<int:treinadorid>/sessoes', TreinadorSessoes.as_view(), name='treinadorsessoes'),
    path('api/treinadores/<int:treinadorid>/atletas', TreinadorAtletas.as_view(), name='treinadoratletas'),
    path('api/atletas/<int:atletaid>/sessoes', AtletaSessoes.as_view(), name='atletasessoes'),
    #path('api/exercicios/', ExercicioList.as_view(), name='exerciciolist'),
    path('api/treinos/', TreinoList.as_view(), name='treinolist'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/', views.obtain_auth_token(), name='get_token'),
    path('api/populardb/', PopularDB.as_view()),
    path('api/makesessao/<int:treinoid>', MakeSessao.as_view(), name='makesessao'),
    path('api/maketempo/<int:sessaoid>', MakeTempo.as_view(), name='maketempo'),
    path('cadastrotreinador', CadastroTreinador.as_view(), name='cadastrotreinador'),
    path('cadastroatleta', CadastroAtleta.as_view(), name='cadastroatleta'),
    #path('registrarexercicio', RegistrarExercicio.as_view(), name='registrarexercicio'),
    path('registrartreino', RegistrarTreino.as_view(), name='registrartreino'),
    path('registrartreinoviaid', RegistrarTreinoViaID.as_view(), name='registrartreinoviaid'),
    path('registraravaliacaotreino', RegistrarAvaliacaoTreino.as_view(), name='registraravaliacaotreino'),
    path('registraravaliacaodireta/<int:treinoid>', RegistrarAvaliacaoDireta.as_view(), name='registraravaliacaodireta'),
    path('logintreinador', LoginTreinador.as_view(), name='logintreinador'),
    path('loginatleta', LoginAtleta.as_view(), name='loginatleta'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('indextreinador', TemplateView.as_view(template_name='indextreinador.html'), name='indextreinador'),
    path('indexatleta', TemplateView.as_view(template_name='indexatleta.html'), name='indexatleta'),
    path('treinadortreinos', TreinadorTreinos.as_view(), name='treinadortreinos'),
    path('atletatreinos', AtletaTreinos.as_view(), name='atletatreinos'),
    path('treinodetalhe/<int:treinoid>', TreinoDetalhe.as_view(), name='treinodetalhe'),
    path('sessaodetalhe/<int:sessaoid>', SessaoDetalhe.as_view(), name='sessaodetalhe'),
    path('chartdemo', TemplateView.as_view(template_name='chartdemo.html'), name='chartdemo'),
    path('line_chart_json', LineChartJSONView.as_view(), name='line_chart_json'),
    path('testchart/<int:treinoid>', SessaoGraphView.as_view(), name='testchart'), # Mostra template renderizando JSON
    path('tempographjson/<int:sessaoid>', TemposGraphJSONView.as_view(), name='tempographjson'), #Retorna um JSON
    path('sessaographjson/<int:treinoid>', SessaoGraphJSONView.as_view(), name='sessaographjson'),  # Retorna um JSON

]
