from flask import Blueprint
from src.utilities import ehandler
from .service import ProxyService
from src.constants import REDIS_ADDRESS, CACHE_CAPACITY, GLOBAL_CACHE_EXPIRY
from flask import jsonify

proxy_controller = Blueprint("proxy_controller", __name__, url_prefix="/proxy")


@proxy_controller.route("/", methods=["GET"])
@ehandler._try
def get():
    """Handle the GET request."""
    proxy_service = ProxyService(
        redis_full_address=REDIS_ADDRESS,
        cache_capacity=CACHE_CAPACITY,
        global_cache_expiry=GLOBAL_CACHE_EXPIRY,
    )

    response_obj = {"cached_value": proxy_service.retrieve_value_for("key")}

    return jsonify(response_obj)
