from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('silogismo/<int:key>/', views.exibir_silogismo, name='exibir_silogismo'),
    path('reducao/<int:key>/', views.reducao, name='reducao'),
    path('contato', views.contato, name='contato'),
    path('avalia', views.avalia, name='avalia'),
]
