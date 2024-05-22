from entities.models import Pedido, PratoPedido, Prato
from unittest import mock


def test_pedido_get(client, session_scope):
    with session_scope() as session:
        pass

    response = client.get("/api/pedido")

    session.query.assert_called_once_with(Pedido)
    session.query().all.assert_called_once()
    assert response.status_code == 200


def test_pedido_get_by_id(client, session_scope):
    with session_scope() as session:
        pass

    pedido_to_search = \
        Pedido(id=1, nome_cliente="Pedido", forma_pagamento="Dinheiro")
    session.add(pedido_to_search)

    response = client.get("/api/pedido/1")

    session.query.assert_called_once_with(Pedido)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome_cliente"] == "Pedido"
    assert response.json["forma_pagamento"] == "Dinheiro"


def test_pedido_set(client, session_scope):
    with session_scope() as session:
        pass

    response = client.post(
            "/api/pedido",
            json={"nome_cliente": "Pedido", "forma_pagamento": "Credito"})

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome_cliente"] == "Pedido"
    assert response.json["forma_pagamento"] == "Credito"


def test_pedido_set_withoud_required(client):
    response = client.post(
            "/api/pedido",
            json={})

    assert response.status_code == 400


def test_pedido_set_withoud_required_2(client):
    response = client.post(
            "/api/pedido",
            json={"nome_cliente": "Pedido1"})

    assert response.status_code == 400


def test_pedido_set_incorrect_forma_pagamento(client):
    response = client.post(
            "/api/pedido",
            json={"nome_cliente": "Pedido1", "forma_pagamento": "pix"})

    assert response.status_code == 400


def test_pedido_delete(client, session_scope):
    with session_scope() as session:
        pass

    pedido_to_delete = \
        Pedido(id=1, nome_cliente="Nome Cliente", forma_pagamento="Debito")
    session.add(pedido_to_delete)

    response = client.delete("/api/pedido/1")

    session.query.assert_has_calls(
            [mock.call(Pedido), mock.call(PratoPedido)], any_order=True)
    session.query().filter().first.assert_called_once()
    session.commit.assert_called_once()
    session.delete.assert_has_calls(
            [mock.call(), mock.call(pedido_to_delete)])
    assert response.status_code == 200
    assert response.json["nome_cliente"] == "Nome Cliente"
    assert response.json["forma_pagamento"] == "Debito"


def test_prato_pedido_get(client, session_scope):
    with session_scope() as session:
        pass

    pedido = \
        Pedido(id=1, nome_cliente="Nome Cliente", forma_pagamento="Dinheiro")
    session.add(pedido)

    response = client.get("/api/pedido/1/prato")

    session.query.assert_called_once_with(Pedido)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    assert response.status_code == 200


def test_prato_pedido_get_preco_quantidade_info(client, session_scope):
    with session_scope() as session:
        pass

    prato_1 = Prato(id=1, nome="Prato 1", preco=12.5)
    prato_pedido_1 = PratoPedido(
            id_pedido=1, id_prato=1, quantidade_prato=2, prato=prato_1)
    prato_2 = Prato(id=2, nome="Prato 2", preco=15.7)
    prato_pedido_2 = PratoPedido(
            id_pedido=1, id_prato=2, quantidade_prato=3, prato=prato_2)
    pedido = Pedido(
            id=1, nome_cliente="Nome Cliente", forma_pagamento="Dinheiro",
            pratos=[prato_pedido_1, prato_pedido_2])
    session.add(pedido)
    session.add(prato_1)
    session.add(prato_pedido_1)
    session.add(prato_2)
    session.add(prato_pedido_2)

    response = client.get("/api/pedido/1")

    session.query.assert_called_once_with(Pedido)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    print(response.json)
    assert response.status_code == 200
    assert response.json["preco_total_pedido"] == 72.1


def test_prato_pedido_set(client, session_scope):
    with session_scope() as session:
        pass

    prato = Prato(id=1, nome="Prato", preco=30.4)
    pedido = Pedido(id=1, nome_cliente="Pedido", forma_pagamento="Dinheiro")
    session.add(pedido)
    session.add(prato)

    response = client.post(
            "/api/pedido/1/prato",
            json={"id_prato": 1, "quantidade_prato": 2})

    session.query.assert_has_calls(
            [mock.call(Pedido), mock.call(Prato)], any_order=True)
    session.add.assert_has_calls(
            [mock.call(mock.ANY), mock.call(mock.ANY), mock.call(mock.ANY)])
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome_cliente"] == "Pedido"
    assert response.json["forma_pagamento"] == "Dinheiro"


def test_prato_pedido_delete(client, session_scope):
    with session_scope() as session:
        pass

    prato_pedido_to_delete = \
        PratoPedido(id_prato=1, id_pedido=1)
    session.add(prato_pedido_to_delete)

    response = client.delete("/api/pedido/1/prato/1")

    session.query.assert_called_once_with(PratoPedido)
    session.query().filter().filter.assert_has_calls(
            [mock.call(mock.ANY, mock.ANY), mock.call()], any_order=True)
    session.query().filter().filter().first.assert_called_once()
    session.commit.assert_called_once()
    session.delete.assert_called_once()
    assert response.status_code == 200
    assert response.json["id_prato"] == 1
    assert response.json["id_pedido"] == 1
    assert response.status_code == 200
