from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('api/clientes', views.ClienteViewSet, basename='api-clientes')

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('usuarios/cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('clientes/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/excluir/', views.excluir_cliente, name='excluir_cliente'),
] + router.urls
