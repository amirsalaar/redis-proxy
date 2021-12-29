from flask import Blueprint


redis_proxy_controller = Blueprint("redis_proxy_controller", __name__, url_prefix="/")


@redis_proxy_controller.route("/")
def get_value():
    pass
