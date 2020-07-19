"""Arquivo onde sao definidas as url's de acesso as funcoes definidas
em views.py."""

from django.urls import path
from api import views

urlpatterns = [
    path('paradasposicao/<int:lat>:<int:lon>/n:<int:n_paradas>/', views.paradas_por_posicao_n),
    path('paradasposicao/<int:lat>:<int:lon>/', views.paradas_por_posicao),
    path('linhasveiculos/', views.veiculos_por_linha_list),
    path('linhasveiculos/id:<int:linha_id>/', views.veiculos_por_linha_detail),
    path('paradaslinhas/', views.linhas_por_parada_list),
    path('paradaslinhas/id:<int:parada_id>/', views.linhas_por_parada_detail),
    path('<str:modelo>/', views.operate_list),
    path('<str:modelo>/id:<int:primary_key>/', views.operate_details),
]
