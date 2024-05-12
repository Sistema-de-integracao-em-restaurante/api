from flask import jsonify, request
from entities.models import Pedido, PratoPedido, Prato
from marshmallow import ValidationError
from schemas.creation import PedidoCreationSchema, PratoPedidoCreationSchema
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

    @bp.get("<int:id>/prato")
    def get_pedido_prato_by_id(id: int):
        with session_scope() as session:
            pedido = session.query(Pedido).filter(Pedido.id == id).first()
            if not pedido:
                return {"error": "Pedido nao encontrado"}, 404
            return jsonify([i.serialize() for i in pedido.pratos])

    @bp.post("<int:id_pedido>/prato")
    def set_pedido_prato(id_pedido: int):
        try:
            request_data = PratoPedidoCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        id_prato = request_data["id_prato"]
        quantidade_prato = request_data["quantidade_prato"]

        with session_scope() as session:
            pedido = session.query(Pedido) \
                    .filter(Pedido.id == id_pedido).first()
            if not pedido:
                return {"error": "Pedido nao encontrado"}, 404

            prato = session.query(Prato).filter(Prato.id == id_prato).first()
            if not prato:
                return {"error": "Prato nao encontrado"}, 404

            pedido_prato = \
                PratoPedido(id_pedido=id_pedido,
                            id_prato=id_prato,
                            quantidade_prato=quantidade_prato)
            session.add(pedido_prato)
            session.commit()
            session.refresh(pedido)
            return jsonify(pedido.serialize())

    @bp.delete("<int:id_pedido>/prato/<int:id_prato>")
    def delete_pedido_prato(id_pedido: int, id_prato: int):
        with session_scope() as session:
            pedido_prato = session.query(PratoPedido) \
                .filter(PratoPedido.id_pedido == id_pedido) \
                .filter(PratoPedido.id_prato == id_prato) \
                .first()
            if not pedido_prato:
                return {"error": "Relacionamento entre prato e "
                        "pedido nao encontrado"}, 404

            session.delete(pedido_prato)
            session.commit()
            return jsonify(pedido_prato.serialize())

    return bp
