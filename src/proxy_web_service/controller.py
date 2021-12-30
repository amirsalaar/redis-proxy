from flask import Blueprint


proxy_controller = Blueprint("proxy_controller", __name__, url_prefix="/")


@proxy_controller.route("/")
def get():
    pass
