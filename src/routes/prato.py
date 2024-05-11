from flask import jsonify, request
from entities.models import Prato, IngredientePrato
from marshmallow import ValidationError
from schemas.prato import PratoCreationSchema
from schemas.ingredienteprato import IngredientePratoCreationSchema
from flask import Blueprint


def build_routes(session):
    bp = Blueprint('bp_prato', __name__)

    @bp.get("/prato")
    def get_pratos():
        pratos = session.query(Prato).all()
        return jsonify([p.serialize() for p in pratos])

    @bp.get("/prato/<int:id>")
    def get_prato_by_id(id: int):
        prato = session.query(Prato).filter(
                Prato.id == id).first()
        if not prato:
            return {"error": "Prato nao encontrado"}, 404
        return jsonify(prato.serialize())

    @bp.post("/prato")
    def set_prato():
        try:
            request_data = PratoCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        nome = request_data["nome"]
        preco = request_data["preco"]
        prato = Prato(nome=nome, preco=preco)
        session.add(prato)
        session.commit()
        session.refresh(prato)
        return jsonify(prato.serialize())

    @bp.delete("/prato/<int:id>")
    def delete_prato(id: int):
        prato = session.query(Prato).filter(Prato.id == id).first()
        if not prato:
            return {"error": "Prato nao encontrado"}, 404

        session.query(IngredientePrato).filter(
                IngredientePrato.id_prato == id).delete()

        session.delete(prato)
        session.commit()
        return jsonify(prato.serialize())

    @bp.get("/prato/<int:id>/ingrediente")
    def get_ingrediente_prato_by_id(id: int):
        prato = session.query(Prato).filter(
                Prato.id == id).first()
        if not prato:
            return {"error": "Prato nao encontrado"}, 404
        return jsonify([i.serialize() for i in prato.ingredientes])

    @bp.post("/prato/<int:id_prato>/ingrediente")
    def set_ingrediente_prato(id_prato: int):
        try:
            request_data = IngredientePratoCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        id_ingrediente = request_data["id_ingrediente"]
        quantidade_ingrediente = request_data["quantidade_ingrediente"]
        prato = session.query(Prato).filter(Prato.id == id_prato).first()
        if not prato:
            return {"error": "Prato nao encontrado"}, 404

        ingrediente_prato = \
            IngredientePrato(id_ingrediente=id_ingrediente,
                             id_prato=id_prato,
                             quantidade_ingrediente=quantidade_ingrediente)
        session.add(ingrediente_prato)
        session.commit()
        session.refresh(prato)
        return jsonify(prato.serialize())

    @bp.delete("/prato/<int:id_prato>/ingrediente/<int:id_ingrediente>")
    def delete_ingrediente_prato(id_prato: int, id_ingrediente: int):
        ingrediente_prato = session.query(IngredientePrato).filter(
                IngredientePrato.id_prato == id_prato and
                IngredientePrato.id_ingrediente == id_ingrediente).first()
        if not ingrediente_prato:
            return {"error": "Relacionamento entre prato e "
                    "ingrediente nao encontrado"}, 404

        session.delete(ingrediente_prato)
        session.commit()
        return jsonify(ingrediente_prato.serialize())

    return bp
