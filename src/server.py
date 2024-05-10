import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from routes.ingrediente import build_routes


def build_app(session):
    app = Flask(__name__)

    app.register_blueprint(build_routes(session))

    @app.route("/")
    def display_app_data():
        return {
                "name": "Restaurant Order API",
                "version": os.getenv("RO_VERSION", "v0.0.0")
        }

    return app


engine = create_engine(os.getenv("DB_CON_STRING", "sqlite:///example.db"))
Session = sessionmaker(bind=engine)
session = Session()
app = build_app(session)
