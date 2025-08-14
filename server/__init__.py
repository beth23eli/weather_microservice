from flask import Flask
from server.extensions import db
from server.routes import weather_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.config.from_object("server.config.Config")
    db.init_app(app)

    CORS(app)

    app.register_blueprint(weather_routes)

    return app
