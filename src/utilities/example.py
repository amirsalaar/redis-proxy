"""This module has some example endpoints for the application."""
from flask import Blueprint
from werkzeug.exceptions import InternalServerError

example_controller = Blueprint("example_controller", __name__, url_prefix="/example")


@example_controller.route("/", methods=["GET"])
def index():
    return "Hello World!"


@example_controller.route("/404", methods=["GET"])
def test_error_handling():
    from werkzeug.exceptions import NotFound

    raise NotFound()


@example_controller.route("/500", methods=["GET"])
def test_generic_server_crash():
    raise InternalServerError()


@example_controller.route("/405", methods=["POST"])
def raise_not_allowed_method():
    return "Opps! Not implemented 405"
