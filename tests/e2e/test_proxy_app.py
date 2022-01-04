"""End to End test of the APP."""
import os
import time
from flask.testing import FlaskClient
from redis import Redis
import pytest
from pytest_mock import MockerFixture

from src.local_cache import LocalCache

if os.getenv("FLASK_ENV") == "production":
    TEST_REDIS_ADDRESS = "redis:6379"
else:
    TEST_REDIS_ADDRESS = "localhost:6379"
CAPACITY = 10
GLOBAL_EXPIRY = 30  # seconds


@pytest.fixture()
def mocked_redis_address(mocker: MockerFixture):
    mocker.patch("src.proxy_web_service.controller.REDIS_ADDRESS", TEST_REDIS_ADDRESS)


@pytest.mark.order1
def test_proxy_app_should_retrieve_key_from_redis_instance(
    test_client: FlaskClient, test_redis_client: Redis, mocked_redis_address
):
    """Test the proxy app workflow.
    This is the initial state of the Backing Redis server and the key doesnt exist on the local cache.
    """
    test_redis_client.set("key1", "value1")

    res = test_client.get("/proxy/", query_string={"key": "key1"})
    assert res.status_code == 200
    assert res.json == {"cached_value": "value1"}


@pytest.mark.order2
def test_proxy_app_should_retrieve_key_from_local_cache_scenario1(
    test_client: FlaskClient, test_redis_client: Redis, mocked_redis_address
):
    """Test key retrieval from local cache.

    We are testing the following scenario:
        - The key is NOT in the local cache and is in the backing redis
            -> on retrieval will be added to local cache.
            -> when trying to get the key again, it will be retrieved from the local cache.
    """
    test_redis_client.set("key2", "value2")

    res = test_client.get("/proxy/", query_string={"key": "key2"})

    test_redis_client.set("key2", "value in redis changed")

    assert res.status_code == 200
    assert res.json == {"cached_value": "value2"}


@pytest.mark.order3
def test_proxy_app_should_retrieve_key_from_local_cache_scenario2(
    mocker: MockerFixture,
    test_client: FlaskClient,
    test_redis_client: Redis,
    mocked_redis_address,
):
    """Test key retrieval from local cache.

    We are testing the following scenario:
        - The key is in the local cache and it is expired.
            -> it retrieves the key from the local cache and removes it due to being expired.
            -> then looks into backing redis for the key and if finds it puts it back into the local cache.
    """
    mocker.patch("src.proxy_web_service.controller.local_cache", LocalCache(10, 3))

    test_redis_client.set("key3", "value3")

    res1 = test_client.get("/proxy/", query_string={"key": "key3"})
    assert res1.json == {"cached_value": "value3"}

    test_redis_client.set("key3", "value in redis changed")
    time.sleep(3)
    res2 = test_client.get("/proxy/", query_string={"key": "key3"})

    assert res2.json == {"cached_value": "value in redis changed"}
