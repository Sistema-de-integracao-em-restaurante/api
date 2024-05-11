import os
from flask import Flask
from routes.ingrediente import build_routes as build_ingrediente_routes
from routes.prato import build_routes as build_prato_routes
from entities.session import session_scope
from flask_cors import CORS


def build_app(session_scope):
    app = Flask(__name__)

    app.register_blueprint(build_ingrediente_routes(session_scope))
    app.register_blueprint(build_prato_routes(session_scope))

    @app.route("/")
    def display_app_data():
        return {
                "name": "Restaurant Order API",
                "version": os.getenv("RO_VERSION", "v0.0.0")
        }

    @app.errorhandler(500)
    def error_handler_500(e):
        with session_scope() as session:
            session.rollback()
            return {"error": "Aconteceu um erro durante o processamento da "
                    "requisicao. Tente novamente mais tarde"}, 500

    return app


app = build_app(session_scope)
CORS(app, supports_credentials=True)
