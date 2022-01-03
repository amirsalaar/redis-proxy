import time
from threading import Lock
from dataclasses import dataclass

from src.local_cache.lru_cache import LRUCache
from src.vars import env_vars_store

GLOBAL_CACHE_EXPIRY = int(env_vars_store.get("GLOBAL_CACHE_EXPIRY", "60"))  # seconds
CACHE_CAPACITY = int(env_vars_store.get("CACHE_CAPACITY", "10"))


# The following mutext has been declared globally to simplify the thread locking.
cache_locker = Lock()


@dataclass
class CacheBox:
    """
    A cache box is a container for a LRUCache with a global expiry.
    The cache might be in use by a thread. So, i order to avoid
    its interferece with other threads, it must be locked when it is used.
    - A locker object field is used to lock the local cache.

    """

    cache: LRUCache
    global_expiry: int  # in seconds


@dataclass
class CachedValue:
    """
    A data structure of the cached values.
    """

    value: any
    expiry: int  # in seconds


class LocalCache:
    """
    This class imlements the local cache.
    """

    def __init__(
        self, capacity: int = CACHE_CAPACITY, global_expiry: int = GLOBAL_CACHE_EXPIRY
    ):
        """Initialize the cache box.

        Args:
            capacity (int): the number of keys in the cache.
            global_expiry (int): the time period of the cache in seconds.
        """
        self.cache_box = CacheBox(cache=LRUCache(capacity), global_expiry=global_expiry)

    def get(self, key: str) -> any:
        """Get the value of the key.

        - if expired, it's removed from the cache
        - if not expired, it's moved to the end of the cache
        """
        global cache_locker
        cache_locker.acquire()
        try:
            cached_value: CachedValue = self.cache_box.cache.get(key)
            if cached_value:
                if self._is_expired(cached_value):
                    self.cache_box.cache.remove(key)
                    return None
                else:
                    return cached_value.value

            return None
        finally:
            cache_locker.release()

    def set(self, key: str, value: any) -> None:
        """Set the key and value into the cache.

        Args:
            key (str): the key to be set.
            value (any): the value to be set.

        Returns:
            None
        """
        now = time.time()
        expiry = now + self.cache_box.global_expiry

        cached_value = CachedValue(value=value, expiry=expiry)
        global cache_locker
        cache_locker.acquire()
        self.cache_box.cache.set(key, cached_value)
        cache_locker.release()

    def _is_expired(self, cached_value: CachedValue) -> bool:
        """Check whether the cached value is expired.

        Args:
            cached_value (CachedValue): the cached value to be checked.
        """
        now = time.time()
        if cached_value.expiry <= now:
            return True

        return False
