def test_lru_cache_get():
    """
    Test the get method of the LRU cache.
    """
    from src.local_cache import LRUCache

    cache = LRUCache(capacity=2)

    cache.set("key1", 1)
    cache.set("key3", 3)
    # order of LRU till this point: [key1, key3]
    cache.get("key1")
    # order of LRU till this point: [key3, key1]
    cache.set("key2", 2)
    # order of LRU till this point: [key1, key2]

    assert cache.get("key3") is None
    assert cache.get("key1") == 1
    assert cache.get("key2") == 2


def test_lru_cache_remove():
    """
    Test the remove method of the LRU cache.
    """
    from src.local_cache import LRUCache

    cache = LRUCache(capacity=2)

    cache.set("key1", 1)
    cache.set("key2", 2)

    cache.remove("key1")

    assert cache.get("key1") is None
    assert cache.get("key2") == 2


def test_lru_cache_set_with_duplicate_key_must_return_the_latest():
    """
    Test the set method of the LRU cache.
    """
    from src.local_cache import LRUCache

    cache = LRUCache(capacity=2)

    cache.set("key1", 1)
    cache.set("key1", 2)

    assert cache.get("key1") == 2
