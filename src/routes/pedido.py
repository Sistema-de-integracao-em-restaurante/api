from flask import jsonify, request
from entities.models import Pedido, PratoPedido
from marshmallow import ValidationError
from schemas.creation import PedidoCreationSchema
from flask import Blueprint


def build_routes(session_scope):
    bp = Blueprint('bp_pedido', __name__)

    @bp.get("")
    def get_pedidos():
        with session_scope() as session:
            pedidos = session.query(Pedido).all()
            return jsonify([p.serialize() for p in pedidos])

    @bp.get("<int:id>")
    def get_pedido_by_id(id: int):
        with session_scope() as session:
            pedido = session.query(Pedido).filter(Pedido.id == id).first()
            if not pedido:
                return {"error": "Pedido nao encontrado"}, 404
            return jsonify(pedido.serialize())

    @bp.post("")
    def set_pedido():
        try:
            request_data = PedidoCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        nome_cliente = request_data["nome_cliente"]
        forma_pagamento = request_data["forma_pagamento"]
        pedido = Pedido(nome_cliente=nome_cliente,
                        forma_pagamento=forma_pagamento)

        with session_scope() as session:
            session.add(pedido)
            session.commit()
            session.refresh(pedido)
            return jsonify(pedido.serialize())

    @bp.delete("<int:id>")
    def delete_pedido(id: int):
        with session_scope() as session:
            pedido = session.query(Pedido).filter(Pedido.id == id).first()
            if not pedido:
                return {"error": "Pedido nao encontrado"}, 404

            session.query(PratoPedido) \
                .filter(PratoPedido.id_pedido == id).delete()

            session.delete(pedido)
            session.commit()
            return jsonify(pedido.serialize())

    return bp
