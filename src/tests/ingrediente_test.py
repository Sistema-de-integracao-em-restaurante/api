from entities.models import Ingrediente


def test_ingrediente_get(client, session_scope):
    response = client.get("/api/ingrediente")

    with session_scope() as session:
        pass

    session.query.assert_called_once_with(Ingrediente)
    session.query().all.assert_called_once()
    assert response.status_code == 200


def test_ingrediente_get_by_id(client, session_scope):
    with session_scope() as session:
        pass

    ingrediente_to_search = \
        Ingrediente(id=1, nome="Ingrediente", descricao="descricao")
    session.query.return_value.filter.return_value \
           .first.return_value \
           .serialize.return_value = ingrediente_to_search.serialize()

    response = client.get("/api/ingrediente/1")

    session.query.assert_called_once_with(Ingrediente)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Ingrediente"
    assert response.json["descricao"] == "descricao"


def test_ingrediente_set(client, session_scope):
    response = client.post(
            "/api/ingrediente",
            json={"nome": "Ingrediente", "descricao": "descricao"})

    with session_scope() as session:
        pass

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Ingrediente"
    assert response.json["descricao"] == "descricao"


def test_ingrediente_set_withoud_unrequired(client, session_scope):
    response = client.post(
            "/api/ingrediente",
            json={"nome": "Ingrediente"})

    with session_scope() as session:
        pass

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Ingrediente"


def test_ingrediente_set_withoud_required(client):
    response = client.post(
            "/api/ingrediente",
            json={})

    assert response.status_code == 400


def test_ingrediente_delete(client, session_scope):
    with session_scope() as session:
        pass

    ingrediente_to_delete = \
        Ingrediente(id=1, nome="Ingrediente", descricao="descricao")
    session.query.return_value.filter.return_value \
           .first.return_value \
           .serialize.return_value = ingrediente_to_delete.serialize()

    response = client.delete("/api/ingrediente/1")

    session.query.assert_called_once_with(Ingrediente)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    session.commit.assert_called_once()
    session.delete.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Ingrediente"
    assert response.json["descricao"] == "descricao"
