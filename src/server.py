import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.ingrediente import Ingrediente


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

    @app.post("/ingrediente")
    def set_ingrediente():
        nome = request.args.get('nome')
        descricao = request.args.get('descricao')
        ingrediente = Ingrediente(nome=nome, descricao=descricao)
        session.add(ingrediente)
        session.commit()
        return "Ingrediente criado com sucesso!"

    return app


engine = create_engine(os.getenv("DB_CON_STRING", ""))
Session = sessionmaker(bind=engine)
session = Session()
app = build_app(session)
