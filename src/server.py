import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.ingrediente import Ingrediente
from marshmallow import ValidationError
from schemas.ingrediente import IngredienteCreationSchema


def build_app(session):
    app = Flask(__name__)

    @app.route("/")
    def display_app_data():
        return {
                "name": "Restaurant Order API",
                "version": os.getenv("RO_VERSION", "v0.0.0")
        }

    @app.get("/ingrediente")
    def get_ingredientes():
        ingredientes = session.query(Ingrediente).all()
        return jsonify([i.serialize() for i in ingredientes])

    @app.get("/ingrediente/<int:id>")
    def get_ingrediente_by_id(id: int):
        ingrediente = session.query(Ingrediente).filter(
                Ingrediente.id == id).first()
        return jsonify(ingrediente.serialize())

    @app.post("/ingrediente")
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

    @app.delete("/ingrediente/<int:id>")
    def delete_ingrediente(id: int):
        ingrediente = session.query(Ingrediente).filter(
                Ingrediente.id == id).first()
        if not ingrediente:
            return "Ingrediente nao encontrado", 404

        session.delete(ingrediente)
        session.commit()
        return jsonify(ingrediente.serialize())

    return app


engine = create_engine(os.getenv("DB_CON_STRING", "sqlite:///example.db"))
Session = sessionmaker(bind=engine)
session = Session()
app = build_app(session)
