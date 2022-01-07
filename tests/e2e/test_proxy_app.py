"""End to End test of the APP."""
import time
from flask.testing import FlaskClient
from redis import Redis
import pytest

from src.constants import CACHE_CAPACITY, GLOBAL_CACHE_EXPIRY


@pytest.mark.order0
def test_proxy_app_throws_handled_error_response_on_invalid_key(
    test_client: FlaskClient,
):
    """Test if NotFound error is returned for non-existing keys."""
    res = test_client.get("/proxy/", query_string={"key": "key100"})
    assert res.status_code == 404
    assert res.json.get("error_type") == "NotFound"
    assert res.json.get("message") == "404 Not Found: Key not found."


@pytest.mark.order1
def test_proxy_app_should_retrieve_key_from_redis_instance(
    test_client: FlaskClient, test_redis_client: Redis
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
    test_client: FlaskClient, test_redis_client: Redis
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
    test_client: FlaskClient,
    test_redis_client: Redis,
):
    """Test key retrieval from local cache.

    We are testing the following scenario:
        - The key is in the local cache and it is expired.
            -> it retrieves the key from the local cache and removes it due to being expired.
            -> then looks into backing redis for the key and if finds it puts it back into the local cache.
    """

    test_redis_client.set("key3", "value3")

    res1 = test_client.get("/proxy/", query_string={"key": "key3"})
    assert res1.json == {"cached_value": "value3"}

    test_redis_client.set("key3", "value in redis changed")
    time.sleep(
        GLOBAL_CACHE_EXPIRY + 1
    )  # sleep for 1 additional second to the globally configured cache expiry time in .env
    res2 = test_client.get("/proxy/", query_string={"key": "key3"})

    assert res2.json == {"cached_value": "value in redis changed"}


@pytest.mark.order4
def test_proxy_app_should_delete_the_lru_cached_key_if_we_hit_cache_key_limit(
    test_client: FlaskClient,
    test_redis_client: Redis,
):
    """Test deletion of a key from the local cache when reaching the capacity.

    Assume that the capacity is 10 and we have 10 keys in the local cache.
    We are testing the following scenario:
        - We request for getting the 11th key that is not in the local cache.
            -> First we need to add all those 10 keys to redis, then query them to put them in the local cache.
            -> To confirm the eviction, we query the key1 to make it LRU.
            -> The 11th key will be added to the local cache and key1 will be evicted.

    """
    # populate Backing Redis:
    for i in range(1, CACHE_CAPACITY + 2):
        test_redis_client.set(f"key{i}", f"value{i}")

    # read from the proxy:
    for i in range(1, CACHE_CAPACITY + 2):
        # all the keys will be added to the local cache, order of LRU: [key1, key2, key3, ...]
        test_client.get("/proxy/", query_string={"key": f"key{i}"})

    # So far key1 has been evicted, cuz it was retrieved at the very beginning and
    # when we sat key11 after reachin the limit of 10, key1 was the LRU.

    # update the key1 value in the backing redis
    test_redis_client.set("key1", "updated value1")

    # get key1
    res2 = test_client.get("/proxy/", query_string={"key": "key1"})

    # we had initially cached 'value1',
    # but since we expect it to be evicted,
    # we dont expect 'key1' have 'value1' anymore:
    assert res2.json != {"cached_value": "value1"}
    assert res2.json == {"cached_value": "updated value1"}
