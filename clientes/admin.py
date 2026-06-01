from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_pessoa', 'telefone', 'cidade', 'estado', 'ativo', 'criado_por')
    search_fields = ('nome', 'email', 'telefone', 'cpf', 'cnpj', 'inscricao_estadual', 'rua', 'bairro', 'cep')
    list_filter = ('ativo', 'tipo_pessoa', 'estado', 'cidade')
