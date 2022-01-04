"""Main module for creating the Flask application."""
from flask import Flask
from flask_cors import CORS
from src.proxy_web_service import proxy_controller as redis_proxy_controller
from src.utilities import generic_error_hanlder, ProxyAppError


def create_app(config_object={}):
    """Create Flask application."""
    app = Flask(__name__)

    app.config.update(**config_object)
    CORS(app, supports_credentials=True)
    app.register_error_handler(ProxyAppError, generic_error_hanlder)
    app.register_error_handler(Exception, generic_error_hanlder)
    app.register_blueprint(redis_proxy_controller)

    return app
