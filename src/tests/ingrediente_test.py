def test_ingrediente_set(client, session):
    response = client.post(
            "/ingrediente",
            data={"nome": "Ingrediente1", "descricao": "desc1"})
    assert response.status_code == 200
    session.add.assert_called_once()
    session.commit.assert_called_once()
