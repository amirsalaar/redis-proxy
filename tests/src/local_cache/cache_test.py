import time


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
