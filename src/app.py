from flask import Flask
from flask_cors import CORS
from src.redis_proxy import redis_proxy_controller


def create_app():
    app = Flask(__name__)
    # app.config.from_object("app.config.setting")
    # app.config.from_object("app.config.secure")
    CORS(app, supports_credentials=True)
    app.register_blueprint(redis_proxy_controller)

    return app
