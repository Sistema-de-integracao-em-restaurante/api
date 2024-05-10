from models.ingrediente import Ingrediente


def test_ingrediente_get(client, session):
    response = client.get("/ingrediente")

    session.query.assert_called_once_with(Ingrediente)
    session.query().all.assert_called_once()
    assert response.status_code == 200


def test_ingrediente_set(client, session):
    response = client.post(
            "/ingrediente",
            json={"nome": "Ingrediente", "descricao": "descricao"})

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Ingrediente"
    assert response.json["descricao"] == "descricao"


def test_ingrediente_delete(client, session):
    # Mock ingrediente to be deleted
    ingrediente_to_delete = \
            Ingrediente(id=1, nome="Ingrediente", descricao="descricao")
    session.query.return_value.filter.return_value \
           .first.return_value \
           .serialize.return_value = ingrediente_to_delete.serialize()

    response = client.delete("/ingrediente/1")

    session.query.assert_called_once_with(Ingrediente)
    session.query().filter.assert_called_once()
    session.query().filter().first.assert_called_once()
    session.commit.assert_called_once()
    session.delete.assert_called_once()
    assert response.status_code == 200
    assert response.json["nome"] == "Ingrediente"
    assert response.json["descricao"] == "descricao"
