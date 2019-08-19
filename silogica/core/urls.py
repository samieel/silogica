from . import views
from django.urls import path

urlpatterns = [
    path('', views.classe, name='classe'),
    path('new/<str:classe>/', views.nclasse, name='nclasse'), 
    path('s/<str:classe>/', views.index, name='index'),
    path('silogismo/<int:key>/', views.exibir_silogismo, name='exibir_silogismo'),
    path('reducao/<int:key>/', views.reducao, name='reducao'),
    path('contato', views.contato, name='contato'),
    path('avalia', views.avalia, name='avalia'),
    path('e_erros', views.e_erro, name='e_erro'),
    path('erros/<str:classe>/', views.erros, name='erros'),
]
