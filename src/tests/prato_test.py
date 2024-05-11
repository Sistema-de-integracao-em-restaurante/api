from entities.models import Prato, IngredientePrato, Ingrediente
from unittest import mock


def test_prato_get(client, session_scope):
    response = client.get("/api/prato")

    with session_scope() as session:
        pass

    session.query.assert_called_once_with(Prato)
    session.query().all.assert_called_once()
    assert response.status_code == 200


def test_prato_get_by_id(client, session_scope):
    with session_scope() as session:
        pass

    prato_to_search = \
        Prato(id=1, nome="Prato", preco=30.5)
    session.query.return_value.filter.return_value \
           .first.return_value \
           .serialize.return_value = prato_to_search.serialize()

    response = client.get("/api/prato/1")

    session.query.assert_called_once_with(Prato)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Prato"
    assert response.json["preco"] == 30.5


def test_prato_set(client, session_scope):
    response = client.post(
            "/api/prato",
            json={"nome": "Prato", "preco": 20.2})

    with session_scope() as session:
        pass

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Prato"
    assert response.json["preco"] == 20.2


def test_prato_set_withoud_required(client):
    response = client.post(
            "/api/prato",
            json={})

    assert response.status_code == 400


def test_prato_set_withoud_required_2(client):
    response = client.post(
            "/api/prato",
            json={"nome": "Prato1"})

    assert response.status_code == 400


def test_prato_delete(client, session_scope):
    with session_scope() as session:
        pass

    prato_to_delete = \
        Prato(id=1, nome="Prato", preco=26.4)
    session.query.return_value.filter.return_value \
           .first.return_value \
           .serialize.return_value = prato_to_delete.serialize()

    response = client.delete("/api/prato/1")

    session.query.assert_has_calls(
            [mock.call(Prato), mock.call(IngredientePrato)], any_order=True)
    session.query().filter().first.assert_called_once()
    session.commit.assert_called_once()
    session.delete.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Prato"
    assert response.json["preco"] == 26.4


def test_ingrediente_prato_get(client, session_scope):
    response = client.get("/api/prato/1/ingrediente")

    with session_scope() as session:
        pass

    session.query.assert_called_once_with(Prato)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    assert response.status_code == 200


def test_ingrediente_prato_set(client, session_scope):
    with session_scope() as session:
        pass

    prato = Prato(id=1, nome="Prato", preco=26.4)
    session.query.return_value.filter.return_value \
           .first.return_value = prato

    response = client.post(
            "/api/prato/1/ingrediente",
            json={"id_ingrediente": 1, "quantidade_ingrediente": 2})

    session.query.assert_has_calls(
            [mock.call(Prato), mock.call(Ingrediente)], any_order=True)
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Prato"
    assert response.json["preco"] == 26.4


def test_ingrediente_prato_delete(client, session_scope):
    with session_scope() as session:
        pass

    ingrediente_prato_to_delete = \
        IngredientePrato(id_ingrediente=1, id_prato=1)
    session.query.return_value.filter.return_value \
           .first.return_value \
           .serialize.return_value = ingrediente_prato_to_delete.serialize()

    response = client.delete("/api/prato/1/ingrediente/1")

    session.query.assert_called_once_with(IngredientePrato)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    session.commit.assert_called_once()
    session.delete.assert_called_once()
    assert response.status_code == 200
    assert response.json["id_ingrediente"] == 1
    assert response.json["id_prato"] == 1
    assert response.status_code == 200
