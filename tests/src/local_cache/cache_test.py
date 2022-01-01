import time
from pytest_mock import MockFixture


def test_local_cache_get():
    """
    Test the get method of the local cache.
    """
    from src.local_cache import LocalCache

    local_cache = LocalCache(capacity=2, global_expiry=5)

    local_cache.set("key1", "value1")
    time.sleep(2)
    assert local_cache.get("key1") == "value1"
    time.sleep(3)
    assert local_cache.get("key1") is None


def test_local_cache_get_with_global_config(mocker: MockFixture):
    """
    Test the get method of the local cache with global config.
    """
    mocker.patch(
        "src.vars.env_vars_store", {"GLOBAL_CACHE_EXPIRY": "5", "CACHE_CAPACITY": "2"}
    )
    from src.local_cache import LocalCache

    local_cache = LocalCache()

    local_cache.set("key1", "value1")
    time.sleep(2)
    assert local_cache.get("key1") == "value1"
    time.sleep(4)
    assert local_cache.get("key1") is None
    local_cache.set("key1", "value1")
    local_cache.set("key2", "value2")
    local_cache.get("key2")
    local_cache.set("key3", "value3")

    assert all(
        key in local_cache.cache_box.cache.get_all_keys() for key in ["key3", "key1"]
    )
