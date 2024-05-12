from flask import jsonify, request
from entities.models import Prato, IngredientePrato, Ingrediente
from marshmallow import ValidationError
from schemas.creation import PratoCreationSchema, \
    IngredientePratoCreationSchema
from flask import Blueprint


def build_routes(session_scope):
    bp = Blueprint('bp_prato', __name__)

    @bp.get("")
    def get_pratos():
        with session_scope() as session:
            pratos = session.query(Prato).all()
            return jsonify([p.serialize() for p in pratos])

    @bp.get("<int:id>")
    def get_prato_by_id(id: int):
        with session_scope() as session:
            prato = session.query(Prato).filter(
                    Prato.id == id).first()
            if not prato:
                return {"error": "Prato nao encontrado"}, 404
            return jsonify(prato.serialize())

    @bp.post("")
    def set_prato():
        try:
            request_data = PratoCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        nome = request_data["nome"]
        preco = request_data["preco"]
        prato = Prato(nome=nome, preco=preco)

        with session_scope() as session:
            session.add(prato)
            session.commit()
            session.refresh(prato)
            return jsonify(prato.serialize())

    @bp.delete("<int:id>")
    def delete_prato(id: int):
        with session_scope() as session:
            prato = session.query(Prato).filter(Prato.id == id).first()
            if not prato:
                return {"error": "Prato nao encontrado"}, 404

            session.query(IngredientePrato).filter(
                    IngredientePrato.id_prato == id).delete()

            session.delete(prato)
            session.commit()
            return jsonify(prato.serialize())

    @bp.get("<int:id>/ingrediente")
    def get_ingrediente_prato_by_id(id: int):
        with session_scope() as session:
            prato = session.query(Prato).filter(
                    Prato.id == id).first()
            if not prato:
                return {"error": "Prato nao encontrado"}, 404
            return jsonify([i.serialize() for i in prato.ingredientes])

    @bp.post("<int:id_prato>/ingrediente")
    def set_ingrediente_prato(id_prato: int):
        try:
            request_data = IngredientePratoCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        id_ingrediente = request_data["id_ingrediente"]
        quantidade_ingrediente = request_data["quantidade_ingrediente"]

        with session_scope() as session:
            prato = session.query(Prato).filter(Prato.id == id_prato).first()
            if not prato:
                return {"error": "Prato nao encontrado"}, 404

            ingrediente = session.query(Ingrediente).filter(
                    Ingrediente.id == id_ingrediente).first()
            if not ingrediente:
                return {"error": "Ingrediente nao encontrado"}, 404

            ingrediente_prato = \
                IngredientePrato(id_ingrediente=id_ingrediente,
                                 id_prato=id_prato,
                                 quantidade_ingrediente=quantidade_ingrediente)
            session.add(ingrediente_prato)
            session.commit()
            session.refresh(prato)
            return jsonify(prato.serialize())

    @bp.delete("<int:id_prato>/ingrediente/<int:id_ingrediente>")
    def delete_ingrediente_prato(id_prato: int, id_ingrediente: int):
        with session_scope() as session:
            ingrediente_prato = session.query(IngredientePrato) \
                .filter(IngredientePrato.id_prato == id_prato) \
                .filter(IngredientePrato.id_ingrediente == id_ingrediente) \
                .first()
            if not ingrediente_prato:
                return {"error": "Relacionamento entre prato e "
                        "ingrediente nao encontrado"}, 404

            session.delete(ingrediente_prato)
            session.commit()
            return jsonify(ingrediente_prato.serialize())

    return bp
