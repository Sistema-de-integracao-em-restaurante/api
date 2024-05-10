![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
<br>
![CI](https://github.com/Sistema-de-integracao-em-restaurante/api/actions/workflows/ci.yml/badge.svg)
![Release](https://github.com/Sistema-de-integracao-em-restaurante/api/actions/workflows/release.yml/badge.svg)

# API Integração em restaurantes

API REST responsável por controlar o armazenamento e recuperação de informações dos restaurantes.

É utilizado o [Koyeb](https://app.koyeb.com/) como plataforma de produção para a API e para o banco de dados.

## Executando com Docker

```bash
docker build --build-arg="DB_CON_STRING=<DB_CON_STRING>" ro .
docker run --rm -it -p 5000:5000 ro
```

## Exemplo de utilização

```bash
$ curl -X GET -H "Content-Type: application/json" localhost:5000/ingrediente -s | jq .
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

## Desenvolvimento

```bash
docker build --target base --tag ro-dev .
docker run --rm -it -v "$(pwd)"/src:/var/app -p 5000:5000 ro-dev bash
flask --app server run --host 0.0.0.0
```

