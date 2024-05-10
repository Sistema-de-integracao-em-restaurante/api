from flask import jsonify, request
from entities.models import Ingrediente
from marshmallow import ValidationError
from schemas.ingrediente import IngredienteCreationSchema
from flask import Blueprint


def build_routes(session):
    bp = Blueprint('bp_ingrediente', __name__)

    @bp.get("/ingrediente")
    def get_ingredientes():
        ingredientes = session.query(Ingrediente).all()
        return jsonify([i.serialize() for i in ingredientes])

    @bp.get("/ingrediente/<int:id>")
    def get_ingrediente_by_id(id: int):
        ingrediente = session.query(Ingrediente).filter(
                Ingrediente.id == id).first()
        return jsonify(ingrediente.serialize())

    @bp.post("/ingrediente")
    def set_ingrediente():
        try:
            request_data = IngredienteCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        nome = request_data["nome"]
        descricao = request_data["descricao"]
        ingrediente = Ingrediente(nome=nome, descricao=descricao)
        session.add(ingrediente)
        session.commit()
        session.refresh(ingrediente)
        return jsonify(ingrediente.serialize())

    @bp.delete("/ingrediente/<int:id>")
    def delete_ingrediente(id: int):
        ingrediente = session.query(Ingrediente).filter(
                Ingrediente.id == id).first()
        if not ingrediente:
            return "Ingrediente nao encontrado", 404

        session.delete(ingrediente)
        session.commit()
        return jsonify(ingrediente.serialize())

    return bp
