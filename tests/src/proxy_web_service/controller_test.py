from flask.testing import FlaskClient

from src.backing_redis import redis_client
from src.constants import REDIS_ADDRESS


def test_get_key(test_client: FlaskClient):
    """Test the get method of the local cache."""
    r = redis_client(redis_address=REDIS_ADDRESS)
    r.set("hello", "world")

    response = test_client.get("/proxy/", query_string={"key": "hello"})

    assert response.status_code == 200
    assert response.json == {"cached_value": "world"}

    r.delete("hello")
