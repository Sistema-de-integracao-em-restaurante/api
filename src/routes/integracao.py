from flask import jsonify, request
from entities.models import Integracao
from marshmallow import ValidationError
from schemas.creation import IntegracaoCreationSchema
from flask import Blueprint


def build_routes(session_scope):
    bp = Blueprint("bp_integracao", __name__)

    @bp.get("")
    def get_integracao():
        with session_scope() as session:
            integracao = session.query(Integracao).first()
            return jsonify(
                integracao.serialize() if integracao is not None else {}
            )

    @bp.post("")
    def set_integracao():
        try:
            request_data = IntegracaoCreationSchema().load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400

        url = request_data["url"]
        integracao = Integracao(url=url)

        with session_scope() as session:
            session.query(Integracao).delete()
            session.add(integracao)
            session.commit()
            session.refresh(integracao)
            return jsonify(integracao.serialize())

    @bp.delete("")
    def delete_integracao():
        with session_scope() as session:
            integracoes = session.query(Integracao).all()
            session.query(Integracao).delete()
            session.commit()
            return jsonify([i.serialize() for i in integracoes])

    return bp
