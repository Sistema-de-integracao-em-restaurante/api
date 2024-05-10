from models.ingrediente import Ingrediente


def test_ingrediente_get(client, session):
    response = client.get("/ingrediente")

    session.query.assert_called_once_with(Ingrediente)
    session.query().all.assert_called_once()
    assert response.status_code == 200


def test_ingrediente_set(client, session):
    response = client.post(
            "/ingrediente",
            json={"nome": "Ingrediente1", "descricao": "desc1"})

    response_content = response.json
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert response.status_code == 200
    assert response_content["nome"] == "Ingrediente1"
    assert response_content["descricao"] == "desc1"
