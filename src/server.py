import os
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.ingrediente import Ingrediente

app = Flask(__name__)

engine = create_engine(os.getenv('DB_CON_STRING', ''))
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/")
def display_app_data():
    return {
            "name": "Restaurant Order API",
            "version": os.getenv('RO_VERSION', 'v0.0.0')
    }


@app.get("/ingrediente")
def get_ingredientes():
    ingredientes = session.query(Ingrediente).all()
    return jsonify([i.serialize() for i in ingredientes])


@app.post("/ingrediente")
def set_ingrediente():
    ingrediente = Ingrediente(nome="Arroz", descricao="Lorem ipsum")
    session.add(ingrediente)
    session.commit()
    return "Ingrediente criado com sucesso!"
