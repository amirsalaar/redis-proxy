"""Tests for proxy controller.py ."""
from flask.testing import FlaskClient

from src.backing_redis import redis_client


def test_get_key(
    test_client: FlaskClient, get_test_redis_address, mocked_redis_address
):
    """Test the get method of the local cache."""
    r = redis_client(redis_address=get_test_redis_address)
    r.set("hello", "world")

    response = test_client.get("/proxy/", query_string={"key": "hello"})

    assert response.status_code == 200
    assert response.json == {"cached_value": "world"}

    r.delete("hello")
