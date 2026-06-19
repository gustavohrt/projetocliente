from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Cliente


class ClienteCompartilhadoWebTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='usuario_web',
            password='SenhaWeb123',
        )
        self.outro_usuario = User.objects.create_user(
            username='outro_usuario_web',
            password='SenhaWeb123',
        )
        self.cliente_outro_usuario = Cliente.objects.create(
            nome='Cliente compartilhado',
            tipo_pessoa=Cliente.PESSOA_FISICA,
            criado_por=self.outro_usuario,
        )

    def test_lista_mostra_clientes_de_outros_usuarios(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get('/')

        self.assertContains(resposta, self.cliente_outro_usuario.nome)

    def test_usuario_pode_ver_cliente_criado_por_outro_usuario(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(f'/clientes/{self.cliente_outro_usuario.id}/')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertContains(resposta, self.cliente_outro_usuario.nome)


class ClienteCompartilhadoAPITests(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='usuario_api',
            password='SenhaApi123',
        )
        self.outro_usuario = User.objects.create_user(
            username='outro_usuario_api',
            password='SenhaApi123',
        )
        self.cliente_usuario = Cliente.objects.create(
            nome='Cliente do usuario',
            tipo_pessoa=Cliente.PESSOA_FISICA,
            criado_por=self.usuario,
        )
        self.cliente_outro_usuario = Cliente.objects.create(
            nome='Cliente de outro usuario',
            tipo_pessoa=Cliente.PESSOA_FISICA,
            criado_por=self.outro_usuario,
        )

    def test_api_exige_usuario_logado(self):
        resposta = self.client.get('/api/clientes/')

        self.assertIn(
            resposta.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_api_lista_clientes_de_todos_os_usuarios(self):
        self.client.force_authenticate(user=self.usuario)

        resposta = self.client.get('/api/clientes/')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        nomes = {cliente['nome'] for cliente in resposta.data}
        self.assertEqual(nomes, {self.cliente_usuario.nome, self.cliente_outro_usuario.nome})

    def test_api_cria_cliente_marcando_usuario_criador(self):
        self.client.force_authenticate(user=self.usuario)

        resposta = self.client.post(
            '/api/clientes/',
            {
                'nome': 'Novo cliente API',
                'tipo_pessoa': Cliente.PESSOA_FISICA,
            },
            format='json',
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        cliente = Cliente.objects.get(nome='Novo cliente API')
        self.assertEqual(cliente.criado_por, self.usuario)
