from django.urls import path
from appt1 import views
urlpatterns = [
    # rota, view responsavel, nome de referencia
    path('',views.home,name='home'),
    path('usuarios/',views.usuarios,name='listagem_usuarios'),
    path('login/',views.login,name='login_usuarios'),
    path('esquecisenha/',views.esqsenha,name='senha_usuarios'),
    path('rg/',views.retornaGraficos,name='dados_estacao'),
    path('ce/',views.confirmar,name='ce'),
]
