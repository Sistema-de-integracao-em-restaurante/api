![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
<br>
![CI](https://github.com/Sistema-de-integracao-em-restaurante/api/actions/workflows/ci.yml/badge.svg)
![Release](https://github.com/Sistema-de-integracao-em-restaurante/api/actions/workflows/release.yml/badge.svg)
[![cov](https://sistema-de-integracao-em-restaurante.github.io/api/coverage.svg)](https://github.com/Sistema-de-integracao-em-restaurante/api/actions)

# API Integração em restaurantes

API REST responsável por controlar o armazenamento e recuperação de informações dos restaurantes.

É utilizado o [Koyeb](https://app.koyeb.com/) como plataforma de produção para a API e para o banco de dados.

O DB utilizado é uma instância do [postgreSQL](https://www.postgresql.org/), hospedada também no [Koyeb](https://app.koyeb.com/). Foi implementada uma estrutura de [migrations](https://en.wikipedia.org/wiki/Schema_migration) para controlar as versões das entidades.

Essa API tem o objetivo de centralizar as informações relacionadas a pedido de um restaurante em apenas um lugar, fornecendo [webhooks](https://pt.wikipedia.org/wiki/Webhook) para que outros sistemas possam tomar decisões baseadas na movimentação dos pedidos.

## Executando com Docker

```bash
docker build --build-arg="DB_CON_STRING=<DB_CON_STRING>" ro .
docker run --rm -it -p 5000:5000 ro
```

## Exemplo de utilização

```bash
$ curl -X GET -H "Content-Type: application/json" localhost:5000/api/ingrediente -s | jq .
```
Resultado:

```json
[
  {
    "created_at": "Thu, 09 May 2024 20:51:47 GMT",
    "descricao": "Lorem ipsum",
    "id": 7,
    "nome": "Arroz"
  }
]

```

### Documentação

A API possui documentação publicada no [GitBook](https://4irmaospucs-organization.gitbook.io/api-ingteracao-em-restaurantes/).

## Desenvolvimento

```bash
docker build --target base --tag ro-dev .
docker run --rm -it -v "$(pwd)"/src:/var/app -p 5000:5000 ro-dev bash
flask --app server run --host 0.0.0.0
```

