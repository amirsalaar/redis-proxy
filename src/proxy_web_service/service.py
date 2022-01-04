"""This service contains the logic to retrieve the data either from the local cache or from the Backing Redis."""
from dataclasses import dataclass

from src.backing_redis import RedisClient
from src.local_cache import LocalCache


@dataclass
class Proxy:
    """A proxy holds reference to the Redis client and the LocalCache."""

    redis_client: RedisClient
    local_cache: LocalCache


class ProxyService:
    """This class is the ProxyService which includes the logic for calling backing redis or local cache."""

    def __init__(
        self, redis_full_address: str, cache_capacity: int, global_cache_expiry: int
    ) -> None:
        """Instantiate the ProxyService.

        Args:
            redis_full_address (str): The full address of the Backing Redis.
            cache_capacity (int): The capacity of the LocalCache.
            global_cache_expiry (int): The global expiry time of the LocalCache in seconds.
        """
        self.proxy = Proxy(
            redis_client=RedisClient(redis_full_address),
            local_cache=LocalCache(cache_capacity, global_cache_expiry),
        )

    def retrieve_value_for(self, key: str):
        """Handle the GET request."""
        return "Hi"
