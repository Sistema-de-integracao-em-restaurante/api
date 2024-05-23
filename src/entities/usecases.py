import requests
from entities.models import Pedido, Integracao


def request_to_integration_url(session, pedido: Pedido) -> None:
    integracao = session.query(Integracao).first()
    if not integracao or not integracao.url:
        return

    requests.post(integracao.url, json=pedido.ingredientes)
