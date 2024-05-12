from entities.models import Pedido, PratoPedido, Prato
from unittest import mock


def test_pedido_get(client, session_scope):
    response = client.get("/api/pedido")

    with session_scope() as session:
        pass

    session.query.assert_called_once_with(Pedido)
    session.query().all.assert_called_once()
    assert response.status_code == 200


def test_pedido_get_by_id(client, session_scope):
    with session_scope() as session:
        pass

    pedido_to_search = \
        Pedido(id=1, nome_cliente="Pedido", forma_pagamento="Dinheiro")
    session.query.return_value.filter.return_value \
           .first.return_value \
           .serialize.return_value = pedido_to_search.serialize()

    response = client.get("/api/pedido/1")

    session.query.assert_called_once_with(Pedido)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome_cliente"] == "Pedido"
    assert response.json["forma_pagamento"] == "Dinheiro"


def test_pedido_set(client, session_scope):
    response = client.post(
            "/api/pedido",
            json={"nome_cliente": "Pedido", "forma_pagamento": "Credito"})

    with session_scope() as session:
        pass

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
    session.query.return_value.filter.return_value \
           .first.return_value \
           .serialize.return_value = pedido_to_delete.serialize()

    response = client.delete("/api/pedido/1")

    session.query.assert_has_calls(
            [mock.call(Pedido), mock.call(PratoPedido)], any_order=True)
    session.query().filter().first.assert_called_once()
    session.commit.assert_called_once()
    session.delete.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome_cliente"] == "Nome Cliente"
    assert response.json["forma_pagamento"] == "Debito"


def test_prato_pedido_get(client, session_scope):
    response = client.get("/api/pedido/1/prato")

    with session_scope() as session:
        pass

    session.query.assert_called_once_with(Pedido)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    assert response.status_code == 200


def test_prato_pedido_set(client, session_scope):
    with session_scope() as session:
        pass

    pedido = Pedido(id=1, nome_cliente="Pedido", forma_pagamento="Dinheiro")
    session.query.return_value.filter.return_value \
           .first.return_value = pedido

    response = client.post(
            "/api/pedido/1/prato",
            json={"id_prato": 1, "quantidade_prato": 2})

    session.query.assert_has_calls(
            [mock.call(Pedido), mock.call(Prato)], any_order=True)
    session.add.assert_called_once()
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
    session.query.return_value.filter.return_value \
           .filter.return_value \
           .first.return_value \
           .serialize.return_value = prato_pedido_to_delete.serialize()

    response = client.delete("/api/pedido/1/prato/1")

    session.query.assert_called_once_with(PratoPedido)
    session.query().filter.assert_called_once()
    session.query().filter().filter.assert_called_once()
    session.query().filter().filter().first.assert_called_once()
    session.commit.assert_called_once()
    session.delete.assert_called_once()
    assert response.status_code == 200
    assert response.json["id_prato"] == 1
    assert response.json["id_pedido"] == 1
    assert response.status_code == 200
