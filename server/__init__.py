from flask import Flask
from server.extensions import db

def create_app():
    app = Flask(__name__)

    app.config.from_object("server.config.Config")
    db.init_app(app)

    return app
