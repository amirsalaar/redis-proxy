def test_lru_cache_get():
    """
    Test the get method of the LRU cache.
    """
    from src.local_cache import LRUCache

    cache = LRUCache(capacity=2)

    cache.put("key1", 1)
    cache.get("key1")  # returns 1 and moves key1 to the end
    cache.put("key2", 2)
    cache.put("key3", 3)  # key2 will be removed

    assert cache.get("key1") == -1
    assert cache.get("key2") == 2
