from django.conf import settings
from django.db import models


class Cliente(models.Model):
    PESSOA_FISICA = 'fisica'
    PESSOA_JURIDICA = 'juridica'
    TIPO_PESSOA_CHOICES = [
        (PESSOA_FISICA, 'Pessoa fisica'),
        (PESSOA_JURIDICA, 'Pessoa juridica'),
    ]
    ESTADO_CHOICES = [
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'),
        ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
        ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
        ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
        ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
        ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'),
    ]

    nome = models.CharField(max_length=120)
    tipo_pessoa = models.CharField(
        'tipo de pessoa',
        max_length=10,
        choices=TIPO_PESSOA_CHOICES,
        default=PESSOA_FISICA,
    )
    email = models.EmailField(blank=True)
    telefone = models.CharField('telefone para contato', max_length=20, blank=True)
    cpf = models.CharField('CPF', max_length=14, blank=True)
    cnpj = models.CharField('CNPJ', max_length=18, blank=True)
    inscricao_estadual = models.CharField('inscricao estadual', max_length=30, blank=True)
    rua = models.CharField(max_length=120, blank=True)
    numero = models.CharField('numero', max_length=20, blank=True)
    bairro = models.CharField(max_length=80, blank=True)
    endereco = models.CharField('complemento', max_length=180, blank=True)
    cidade = models.CharField(max_length=80, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, blank=True)
    cep = models.CharField('CEP', max_length=9, blank=True)
    ativo = models.BooleanField('cliente ativo', default=True)
    observacoes = models.TextField('observacoes', blank=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clientes',
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome
