from flask import jsonify, request
from flask_cors import cross_origin
from entities.models import Ingrediente
from marshmallow import ValidationError
from schemas.ingrediente import IngredienteCreationSchema
from flask import Blueprint


def build_routes(session_scope):
    bp = Blueprint('bp_ingrediente', __name__)

    @bp.get("")
    def get_ingredientes():
        with session_scope() as session:
            ingredientes = session.query(Ingrediente).all()
            return jsonify([i.serialize() for i in ingredientes])

    @bp.get("<int:id>")
    def get_ingrediente_by_id(id: int):
        with session_scope() as session:
            ingrediente = session.query(Ingrediente).filter(
                    Ingrediente.id == id).first()
            if not ingrediente:
                return {"error": "Ingrediente nao encontrado"}, 404
            return jsonify(ingrediente.serialize())

    @bp.route("", methods=["POST"])
    def set_ingrediente():
        try:
            request_data = IngredienteCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        nome = request_data["nome"]
        descricao = request_data["descricao"]
        ingrediente = Ingrediente(nome=nome, descricao=descricao)

        with session_scope() as session:
            session.add(ingrediente)
            session.commit()
            session.refresh(ingrediente)
            return jsonify(ingrediente.serialize())

    @bp.delete("<int:id>")
    def delete_ingrediente(id: int):
        with session_scope() as session:
            ingrediente = session.query(Ingrediente).filter(
                    Ingrediente.id == id).first()
            if not ingrediente:
                return {"error": "Ingrediente nao encontrado"}, 404

            session.delete(ingrediente)
            session.commit()
            return jsonify(ingrediente.serialize())

    return bp
