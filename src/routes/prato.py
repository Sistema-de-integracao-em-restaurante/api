from flask import jsonify, request
from models.prato import Prato, IngredientePrato
from flask import Blueprint


def build_routes(session):
    bp = Blueprint('bp_prato', __name__)

    @bp.get("/prato")
    def get_pratos():
        pratos = session.query(Prato).all()
        return jsonify([p.serialize() for p in pratos])

    @bp.post("/prato")
    def set_prato():
        request_data = request.json
        nome = request_data["nome"]
        preco = request_data["preco"]
        prato = Prato(nome=nome, preco=preco)
        session.add(prato)
        session.commit()
        session.refresh(prato)
        return jsonify(prato.serialize())

    @bp.post("/prato/<int:id_prato>/ingrediente")
    def set_ingrediente_prato(id_prato: int):
        request_data = request.json
        id_ingrediente = request_data["id_ingrediente"]
        quantidade_ingrediente = request_data["quantidade_ingrediente"]
        prato = session.query(Prato).filter(Prato.id == id_prato).first()
        ingrediente_prato = \
            IngredientePrato(idIngrediente=id_ingrediente,
                             idPrato=id_prato,
                             quantidadeIngrediente=quantidade_ingrediente)
        session.add(ingrediente_prato)
        session.commit()
        session.refresh(prato)
        return jsonify(prato.serialize())

    return bp
