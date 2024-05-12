import os
from flask import Flask
from routes.ingrediente import build_routes as build_ingrediente_routes
from routes.prato import build_routes as build_prato_routes
from routes.pedido import build_routes as build_pedido_routes
from entities.session import session_scope
from flask_cors import CORS


def build_app(session_scope):
    app = Flask(__name__)
    bp_ingrediente = build_ingrediente_routes(session_scope)
    bp_prato = build_prato_routes(session_scope)
    bp_pedido = build_pedido_routes(session_scope)

    cors_resources = {r'/api/*': {'origins': 'http://localhost:3000',
                                  "allow_headers": "*", "expose_headers": "*"}}

    CORS(app, resources=cors_resources, supports_credentials=True)

    with app.app_context():
        app.register_blueprint(bp_ingrediente, url_prefix="/api/ingrediente")
        app.register_blueprint(bp_prato, url_prefix="/api/prato")
        app.register_blueprint(bp_pedido, url_prefix="/api/pedido")

    @app.route("/api")
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
