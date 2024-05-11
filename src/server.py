import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from routes.ingrediente import build_routes as build_ingrediente_routes
from routes.prato import build_routes as build_prato_routes


def build_app(session):
    app = Flask(__name__)

    app.register_blueprint(build_ingrediente_routes(session))
    app.register_blueprint(build_prato_routes(session))

    @app.route("/")
    def display_app_data():
        return {
                "name": "Restaurant Order API",
                "version": os.getenv("RO_VERSION", "v0.0.0")
        }

    @app.errorhandler(500)
    def error_handler_500(e):
        session.rollback()
        return {"error": "Aconteceu um erro durante o processamento da "
                "requisicao. Tente novamente mais tarde"}, 500

    return app


engine = create_engine(os.getenv("DB_CON_STRING", "sqlite:///example.db"))
Session = sessionmaker(bind=engine)
session = Session()
app = build_app(session)
