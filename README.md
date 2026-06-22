# Projeto Cliente

Sistema web em Django para cadastro, consulta, edicao e exclusao de clientes, com API REST para integracao com outros grupos.

## Tecnologias

- Python
- Django 5.2 LTS
- Django REST Framework
- SQLite

## Como rodar o projeto

1. Clone o repositorio:

```bash
git clone https://github.com/gustavohrt/projetocliente.git
cd projetocliente
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependencias:

```bash
pip install -r requirements.txt
```

O projeto esta configurado com Django 5.2 LTS para funcionar tambem com Python 3.10, que e uma versao comum nos ambientes do PythonAnywhere.

4. Crie o banco de dados:

```bash
python manage.py migrate
```

5. Crie um usuario para acessar o sistema:

```bash
python manage.py createsuperuser
```

Tambem e possivel criar usuario pela tela:

```text
http://127.0.0.1:8000/usuarios/cadastrar/
```

6. Rode o servidor:

```bash
python manage.py runserver
```

7. Acesse no navegador:

```text
http://127.0.0.1:8000/
```

## Funcionamento

O sistema exige login para acessar clientes. Qualquer usuario cadastrado e logado consegue ver os mesmos clientes cadastrados.

O campo `criado_por` fica salvo para registrar quem cadastrou o cliente, mas ele nao limita a consulta. Isso permite que outros usuarios e outros grupos integrem com a mesma base de clientes.

## Rotas principais da tela

| Metodo | Rota | Descricao |
| --- | --- | --- |
| GET | `/` | Lista clientes |
| GET/POST | `/usuarios/cadastrar/` | Cadastro de usuario |
| GET/POST | `/login/` | Login |
| POST | `/sair/` | Logout |
| GET/POST | `/clientes/novo/` | Cadastro de cliente |
| GET | `/clientes/<id>/` | Detalhes do cliente |
| GET/POST | `/clientes/<id>/editar/` | Edicao do cliente |
| GET/POST | `/clientes/<id>/excluir/` | Exclusao do cliente |

## API REST

A API fica disponivel em:

```text
http://127.0.0.1:8000/api/clientes/
```

A API exige autenticacao. Para testes e integracao, pode ser usado usuario e senha cadastrados no Django.

### Endpoints

| Metodo | Endpoint | Descricao |
| --- | --- | --- |
| GET | `/api/clientes/` | Lista todos os clientes |
| POST | `/api/clientes/` | Cria um cliente |
| GET | `/api/clientes/<id>/` | Busca um cliente pelo ID |
| PUT | `/api/clientes/<id>/` | Atualiza todos os dados de um cliente |
| PATCH | `/api/clientes/<id>/` | Atualiza parte dos dados de um cliente |
| DELETE | `/api/clientes/<id>/` | Remove um cliente |

### Campos do cliente

| Campo | Tipo | Obrigatorio | Observacao |
| --- | --- | --- | --- |
| `id` | numero | nao | Gerado automaticamente |
| `nome` | texto | sim | Nome do cliente |
| `tipo_pessoa` | texto | nao | `fisica` ou `juridica` |
| `email` | texto | nao | Email do cliente |
| `telefone` | texto | nao | Telefone para contato |
| `cpf` | texto | nao | Usado para pessoa fisica |
| `cnpj` | texto | nao | Usado para pessoa juridica |
| `inscricao_estadual` | texto | nao | Usado para pessoa juridica |
| `rua` | texto | nao | Rua |
| `numero` | texto | nao | Numero |
| `bairro` | texto | nao | Bairro |
| `cidade` | texto | nao | Cidade |
| `estado` | texto | nao | UF com 2 letras |
| `cep` | texto | nao | CEP |
| `endereco` | texto | nao | Complemento |
| `ativo` | booleano | nao | Padrao: `true` |
| `observacoes` | texto | nao | Observacoes gerais |
| `criado_por` | numero | nao | Usuario que criou, preenchido automaticamente |
| `criado_em` | data/hora | nao | Data de criacao, preenchida automaticamente |

### Exemplo de cadastro pela API

```bash
curl -u usuario:senha -X POST http://127.0.0.1:8000/api/clientes/ \
  -H "Content-Type: application/json" \
  -d "{
    \"nome\": \"Cliente Exemplo\",
    \"tipo_pessoa\": \"fisica\",
    \"email\": \"cliente@email.com\",
    \"telefone\": \"11999999999\",
    \"cpf\": \"123.456.789-00\",
    \"cidade\": \"Sao Paulo\",
    \"estado\": \"SP\",
    \"cep\": \"01001-000\",
    \"ativo\": true
  }"
```

### Exemplo de resposta

```json
{
  "id": 1,
  "nome": "Cliente Exemplo",
  "tipo_pessoa": "fisica",
  "email": "cliente@email.com",
  "telefone": "11999999999",
  "cpf": "123.456.789-00",
  "cnpj": "",
  "inscricao_estadual": "",
  "rua": "",
  "numero": "",
  "bairro": "",
  "cidade": "Sao Paulo",
  "estado": "SP",
  "cep": "01001-000",
  "endereco": "",
  "ativo": true,
  "observacoes": "",
  "criado_por": 1,
  "criado_em": "2026-06-19T10:00:00-03:00"
}
```

## Testes

Para rodar os testes:

```bash
python manage.py test
```

## Observacao para integracao

Todos os usuarios autenticados acessam a mesma lista de clientes. Portanto, um cliente cadastrado por um usuario aparece para os outros usuarios logados e tambem na API.

## Publicacao no PythonAnywhere

No Bash do PythonAnywhere, apos criar o API token na pagina Account, rode:

```bash
pip install --user pythonanywhere
```

Depois:

```bash
pa_autoconfigure_django.py https://github.com/gustavohrt/projetocliente.git --python=3.10
```

Ao final, acesse:

```text
https://gustavohrt.pythonanywhere.com/
```
