import re


def test_default_route(client):
    response = client.get("/api")
    assert response.status_code == 200
    assert (
        response.json["name"] == "Restaurant Order API"
    ), "Application name does not match"
    assert re.match(
        r"v(\d+\.)(\d+\.)(\*|\d+)", response.json["version"]
    ), "Regular expression pattern does not match the string"
