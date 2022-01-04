from flask import Blueprint
from src.utilities import ehandler

proxy_controller = Blueprint("proxy_controller", __name__, url_prefix="/proxy")


@proxy_controller.route("/", methods=["GET"])
@ehandler._try
def get():
    raise Exception("Test Exception")
