import pytest


def test_redis_client_throws_error_on_improper_connection():
    from src.backing_redis import redis_client

    with pytest.raises(
        ConnectionError, match="(Connection to Backing Redis refused).*"
    ):
        redis_client("random_host:6379")

    with pytest.raises(ValueError, match="(Invalid redis address format).*"):
        redis_client("redis=6379")


def test_get_a_key_val_from_backing_redis(get_test_redis_address):
    from src.backing_redis import get, redis_client

    client = redis_client(get_test_redis_address)

    client.set("test_key2", "value2")

    assert not get("test_key", client)
    assert get("test_key2", client) == "value2"

    client.delete("test_key2")


def test_wrapper_class(get_test_redis_address):
    from src.backing_redis import RedisClient

    client = RedisClient(get_test_redis_address)

    client.instance.set("test_key2", "value2")

    assert not client.get("test_key")
    assert client.get("test_key2") == "value2"

    client.instance.delete("test_key2")
