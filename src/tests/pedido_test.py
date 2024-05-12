from entities.models import Pedido, PratoPedido
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
        Pedido(id=1, nome_cliente="Pedido", forma_pagamento="Debito")
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
    assert response.json["nome_cliente"] == "Pedido"
    assert response.json["forma_pagamento"] == "Debito"
