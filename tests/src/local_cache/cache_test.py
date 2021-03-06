import time
from pytest_mock import MockFixture
import pytest


@pytest.mark.order1
def test_local_cache_get_with_global_config(mocker: MockFixture):
    """Test the get method of the local cache with global config."""
    from src.local_cache import LocalCache

    local_cache = LocalCache(capacity=2, global_expiry=5)

    local_cache.set("key1", "value1")
    time.sleep(2)
    assert local_cache.get("key1") == "value1"
    time.sleep(4)
    assert local_cache.get("key1") is None
    local_cache.set("key1", "value1")
    local_cache.set("key2", "value2")
    # make key1 LEAST recently used:
    local_cache.get("key2")
    # key1 will be evicted:
    local_cache.set("key3", "value3")
    assert all(
        key in local_cache.cache_container.cache.get_all_keys()
        for key in ["key3", "key2"]
    )


@pytest.mark.order2
def test_local_cache_get():
    """Test the get method of the local cache."""
    from src.local_cache import LocalCache

    local_cache = LocalCache(capacity=2, global_expiry=5)

    local_cache.set("key1", "value1")
    time.sleep(1)
    assert local_cache.get("key1") == "value1"
    time.sleep(5)
    assert local_cache.get("key1") is None
