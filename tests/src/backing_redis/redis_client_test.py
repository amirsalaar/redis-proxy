import pytest


def test_redis_client_throws_error_on_improper_connection():
    from src.backing_redis import redis_client

    with pytest.raises(
        ConnectionError, match="(Connection to Backing Redis refused).*"
    ):
        redis_client("random_host:6379")


def test_get_a_key_val_from_backing_redis():
    from src.backing_redis import get, redis_client

    client = redis_client("localhost:6379")

    client.set("test_key2", "value2")

    assert not get("test_key", client)
    assert get("test_key2", client) == "value2"

    client.delete("test_key2")
