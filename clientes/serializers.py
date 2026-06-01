from rest_framework import serializers

from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nome',
            'tipo_pessoa',
            'email',
            'telefone',
            'cpf',
            'cnpj',
            'inscricao_estadual',
            'rua',
            'numero',
            'bairro',
            'cidade',
            'estado',
            'cep',
            'endereco',
            'ativo',
            'observacoes',
            'criado_por',
            'criado_em',
        ]
        read_only_fields = ['id', 'criado_por', 'criado_em']
