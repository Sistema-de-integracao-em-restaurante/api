from entities.models import Integracao
from unittest import mock


def test_integracao_get(client, session_scope):
    with session_scope() as session:
        pass

    integracao_to_search = Integracao(
        id=1,
        url="https://example.com",
    )
    session.add(integracao_to_search)

    response = client.get("/api/integracao")

    session.query.assert_called_once_with(Integracao)
    session.query().first.assert_called_once()
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json["url"] == "https://example.com"


def test_integracao_set(client):
    response = client.post(
        "/api/integracao", json={"url": "https://other-example.com"}
    )

    assert response.status_code == 200
    assert response.json["url"] == "https://other-example.com"


def test_integracao_set_invalid_url(client):
    response = client.post("/api/integracao", json={"url": "invalid-url"})
    assert response.status_code == 400


def test_integracao_set_without_required(client):
    response = client.post("/api/integracao", json={})
    assert response.status_code == 400


def test_integracao_delete(client, session_scope):
    with session_scope() as session:
        pass

    integracao_to_delete = Integracao(
        id=1,
        url="https://some-url.com",
    )
    session.add(integracao_to_delete)

    response = client.delete("/api/integracao")

    session.query.assert_has_calls(
        [mock.call(Integracao), mock.call(Integracao)]
    )
    session.query().all.assert_called_once()
    session.commit.assert_called_once()
    assert response.status_code == 200
