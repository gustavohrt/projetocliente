import re

from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
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
        ]
        widgets = {
            'cpf': forms.TextInput(attrs={'maxlength': 14, 'inputmode': 'numeric', 'placeholder': '000.000.000-00'}),
            'cnpj': forms.TextInput(attrs={'maxlength': 18, 'inputmode': 'numeric', 'placeholder': '00.000.000/0000-00'}),
            'cep': forms.TextInput(attrs={'maxlength': 9, 'inputmode': 'numeric', 'placeholder': '00000-000'}),
            'observacoes': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_pessoa = cleaned_data.get('tipo_pessoa')
        cnpj = cleaned_data.get('cnpj')
        cpf = cleaned_data.get('cpf')
        cep = cleaned_data.get('cep')
        inscricao_estadual = cleaned_data.get('inscricao_estadual')
        cpf_digitos = re.sub(r'\D', '', cpf or '')
        cnpj_digitos = re.sub(r'\D', '', cnpj or '')
        cep_digitos = re.sub(r'\D', '', cep or '')

        if cpf and len(cpf_digitos) != 11:
            self.add_error('cpf', 'CPF deve ter 11 digitos.')

        if cnpj and len(cnpj_digitos) != 14:
            self.add_error('cnpj', 'CNPJ deve ter 14 digitos.')

        if cep and len(cep_digitos) != 8:
            self.add_error('cep', 'CEP deve ter 8 digitos.')

        if tipo_pessoa == Cliente.PESSOA_JURIDICA and not cnpj_digitos:
            self.add_error('cnpj', 'Informe o CNPJ para pessoa juridica.')

        if inscricao_estadual and tipo_pessoa != Cliente.PESSOA_JURIDICA:
            self.add_error(
                'inscricao_estadual',
                'Inscricao estadual deve ser usada para cliente com CNPJ.',
            )

        return cleaned_data
